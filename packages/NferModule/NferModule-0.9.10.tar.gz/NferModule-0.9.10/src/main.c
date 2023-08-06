/*
 * main.c
 *
 *  Created on: Jan 19, 2017
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2017  Sean Kauffman
 *
 *   This file is part of nfer.
 *   nfer is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include "types.h"
#include "log.h"
#include "learn.h"
#include "analysis.h"
#include "pool.h"
#include "file.h"
#include "dsl.h"
#include "strings.h"
#include "nfer.h"
#include "debug.h"

#ifdef COMPILER
#include "compile.h"
#endif

#define MAX_EVENT_FILENAME 255
#define MAX_SPEC_FILENAME 255
#define MAX_SPEC_NAME 7

extern timestamp opt_window_size;
extern bool opt_most_recent;
extern bool opt_full;

// unfortunately, we have no way to get the length of optarg.  Just hard code a number.
// this is the max length we will use to parse numbers
#define MAX_LENGTH_OPTARG 20

#define OPTION_CONFIDENCE 500
#define OPTION_SUPPORT 501
static int verbose_flag = 0;
// we want to keep this flag so we don't have to skip code that tests for false
static int compile_flag = 0;

static struct option options[] = {
        /* These options set a flag. */
        { "verbose", no_argument, &verbose_flag, 1 },
#ifdef COMPILER
        { "compile", no_argument, &compile_flag, 1 },
#endif
        /* These options don’t set a flag.  We distinguish them by their indices. */
        { "log-level", required_argument, 0, 'l' },
        { "event-file", required_argument, 0, 'e' },
        { "full", no_argument, 0, 'f'},
        { "groups", no_argument, 0, 'g'},
        { "confidence", required_argument, 0, OPTION_CONFIDENCE },
        { "most-recent", no_argument, 0, 'm' },
        { "support", required_argument, 0, OPTION_SUPPORT },
        { "window", required_argument, 0, 'w' },
        { "help", no_argument, 0, '?' },
        { 0, 0, 0, 0 }
};


int main(int argc, char *argv[]) {
    int c;
    int intarg;
    int option_index;

    pool result_pool, *preloaded_start_pools = NULL;
    dictionary name_dict, key_dict, val_dict;
    nfer_specification spec;
    bool pool_loaded = false, spec_loaded = false;

    unsigned int event_files = 0, event_files_loaded = 0, pool_index;
    char *event_filenames = NULL, *event_filenames_realloc = NULL;
    bool load_spec_file = false;
    char spec_filename[MAX_SPEC_FILENAME + 1];
    bool help = true;
    float confidence = DEFAULT_CONFIDENCE, support = DEFAULT_SUPPORT;
    // for reading from stdin
    char line[MAX_LINE_LENGTH];
    pool input_pool;
    int line_number;
    bool read_success;
    bool output_groups = false;
#ifdef COMPILER
    char *dot_position;
#endif

    while ((c = getopt_long(argc, argv, "cl:e:w:fgmvr?", options, &option_index)) != -1) {
        switch (c) {
#ifdef COMPILER
        case 'c':
            // same as compile flag
            compile_flag = 1;
            break;
#endif
        case OPTION_CONFIDENCE:
            confidence = (float)string_to_double(optarg, MAX_LENGTH_OPTARG);
            break;
        case 'e':
            help = false;
            // copy event file names into an array to load later
            if (event_files == 0) {
                event_filenames = (char *)malloc(sizeof(char) * (MAX_EVENT_FILENAME + 1));
            } else {
                event_filenames_realloc = (char *)realloc(event_filenames, sizeof(char) * (MAX_EVENT_FILENAME + 1) * (event_files + 1));
                // check the return value so we don't accidentally leak memory
                if (event_filenames_realloc) {
                    event_filenames = event_filenames_realloc;
                } else {
                    // if we couldn't realloc, free the currently held memory
                    free(event_filenames);
                    event_filenames = NULL;
                }
            }

            if (event_filenames) {
                copy_string(&event_filenames[event_files * (MAX_EVENT_FILENAME + 1)], optarg, MAX_EVENT_FILENAME);
                event_files++;
            } else {
                // else we failed to allocate memory for the file names...
                event_files = 0;
            }
            break;
        case 'f':
            opt_full = true;
            break;
        case 'g':
            output_groups = true;
            break;
        case 'l':
            intarg = (int)string_to_i64(optarg, MAX_LENGTH_OPTARG);
            set_log_level(intarg);
            break;
        case 'm':
            opt_most_recent = true;
            break;
        case OPTION_SUPPORT:
            support = (float)string_to_double(optarg, MAX_LENGTH_OPTARG);
            break;
        case 'v':
            // same as verbose
            verbose_flag = 1;
            break;
        case 'w':
            opt_window_size = string_to_u64(optarg, MAX_LENGTH_OPTARG);
            break;
        case '?':
            help = true;
            break;
        //default:

        }
    }

    // override the log level
    if (verbose_flag) {
        set_log_level(LOG_LEVEL_DEBUG);
    }

    if (optind < argc) {
        while (optind < argc) {
            // for the moment anyway, just use the last one
            copy_string(spec_filename, argv[optind++], MAX_SPEC_FILENAME);
            load_spec_file = true;
            help = false;
        }
    }

    if (help) {
        // just use fprintf directly, since we want to be sure it goes to stderr
        fprintf(stderr, "nfer  version %s  built %s %s\n", NFER_VERSION, __DATE__, __TIME__);
        fprintf(stderr, "Usage: nfer [OPTIONS] [specification file]\n");
        fprintf(stderr, "\nMandatory arguments to long options are mandatory for short options too.\n");
#ifdef COMPILER
        fprintf(stderr, "  -c  --compile                 compile a monitor for RT applications - produces a C file\n");
#endif
        fprintf(stderr, "      --confidence=CONFIDENCE   set the confidence threshold for the learner\n");
        fprintf(stderr, "  -e, --event-file=FILENAME     set the file name of the event log to process\n");
        fprintf(stderr, "  -f, --full                    return the full set of results by not applying the minimality constraint\n");
        fprintf(stderr, "  -g, --groups                  output interval groups derived from the specification\n");
        fprintf(stderr, "  -?, --help                    print this help message\n");
        fprintf(stderr, "  -l, --log-level=LEVEL         set log level (%d-%d), default is %d, verbose is %d\n",
                LOG_LEVEL_NONE, LOG_LEVEL_SUPERDEBUG, DEFAULT_LOG_LEVEL, LOG_LEVEL_DEBUG);
        fprintf(stderr, "  -m, --most-recent             only use the most recent interval in the trace\n");
        fprintf(stderr, "      --support=SUPPORT         set the support threshold for the learner\n");
        fprintf(stderr, "  -v, --verbose                 set the log level to %d\n", LOG_LEVEL_DEBUG);
        fprintf(stderr, "  -w, --window=SIZE             only match intervals within a window of the specified SIZE\n");
        fprintf(stderr, "Event logs are one event per line, where each line has the following format: EVENT_NAME|TIMESTAMP.\n");
        fprintf(stderr, "Use EVENT_NAME|TIMESTAMP|MAPKEYS|MAPVALUES to include data where MAPKEYS and MAPVALUES are ; delimited lists.\n");
        fprintf(stderr, "See http://nfer.io/ for documentation, updates, bug reports, and feature requests.\n");

    } else {
        // initialize starting data structures
        filter_log_msg(LOG_LEVEL_INFO, "Initializing dictionaries\n");
        initialize_dictionary(&name_dict);
        initialize_dictionary(&key_dict);
        initialize_dictionary(&val_dict);

        // try to load a specification first
        // if no spec is loaded, then we'll use the learner later
        if (load_spec_file) {
            filter_log_msg(LOG_LEVEL_STATUS, "Specification file: %s\n", spec_filename);
            filter_log_msg(LOG_LEVEL_INFO, "Initializing spec\n");
            initialize_specification(&spec, 0);

            spec_loaded = load_specification(spec_filename, &spec, &name_dict, &key_dict, &val_dict);
            if (should_log(LOG_LEVEL_INFO)) {
                log_specification(&spec, &name_dict, &key_dict, &val_dict);
            }
            if (output_groups) {
                log_event_groups(&spec, &name_dict);
            }
#ifdef COMPILER
            // if we want to compile, call the compile routine
            if (compile_flag) {
                // compute spec filename
                // first find the dot or, if none exists, the end
                dot_position = spec_filename;
                while(*dot_position != '.' && *dot_position != '\0') {
                    dot_position++;
                }
                // we have to add three characters
                if (dot_position - spec_filename < MAX_SPEC_FILENAME - 2) {
                    // stick on .c
                    *dot_position++ = '.';
                    *dot_position++ = 'c';
                    *dot_position = '\0';

                    compile_monitor(spec_filename, &spec, &name_dict, &key_dict, &val_dict);
                } else {
                    // otherwise just use monitor.c
                    compile_monitor("monitor.c", &spec, &name_dict, &key_dict, &val_dict);
                }
            }
#endif

        }

        // if the command line included event files to load
        // we need to support loading event files this way so we can handle multiple disparate traces
        if (event_files) {
            filter_log_msg(LOG_LEVEL_STATUS, "Loading event %d files\n", event_files);

            preloaded_start_pools = (pool *)malloc(sizeof(pool) * event_files);
            event_files_loaded = 0;

            // load the files into pools
            for (pool_index = 0; pool_index < event_files; pool_index++) {
                filter_log_msg(LOG_LEVEL_INFO, "Loading event file %s\n", &event_filenames[pool_index * (MAX_EVENT_FILENAME + 1)]);
                initialize_pool(&preloaded_start_pools[event_files_loaded]);
                pool_loaded = read_event_file(&event_filenames[pool_index * (MAX_EVENT_FILENAME + 1)], &preloaded_start_pools[event_files_loaded], &name_dict, &key_dict, &val_dict, spec_loaded);
                if (pool_loaded) {
                    event_files_loaded++;
                    filter_log_msg(LOG_LEVEL_INFO, "Successfully loaded event file into pool\n");
                } else {
                    destroy_pool(&preloaded_start_pools[event_files_loaded]);
                    filter_log_msg(LOG_LEVEL_INFO, "An error occurred loading event file into pool\n");
                }
            }

            // if pools were successfully loaded, then run either a spec or the learner on the preloaded pools
            if (event_files_loaded) {
                if (should_log(LOG_LEVEL_DEBUG)) {
                    log_words(&name_dict);
                }

                if (spec_loaded) {
                    filter_log_msg(LOG_LEVEL_INFO, "Initializing result pool\n");
                    initialize_pool(&result_pool);

                    // resize the spec before running
                    resize_specification(&spec, name_dict.size);

                    filter_log_msg(LOG_LEVEL_STATUS, "Running nfer on preloaded pool...\n");

                    run_nfer(&spec, preloaded_start_pools, &result_pool);
                    output_pool(&result_pool, &name_dict, &key_dict, &val_dict, WRITE_OUTPUT);

                    destroy_pool(&result_pool);

                } else {
                    filter_log_msg(LOG_LEVEL_STATUS, "Running learner...\n");

                    initialize_specification(&spec, name_dict.size);
                    run_learner_on_pool(preloaded_start_pools, event_files_loaded, &name_dict, &key_dict, &val_dict, &spec, confidence, support);
                    output_specification(&spec, &name_dict, &key_dict, &val_dict);
                    if (output_groups) {
                        log_event_groups(&spec, &name_dict);
                    }
                    destroy_specification(&spec);
                }

                // this should be safe...
                for (pool_index = 0; pool_index < event_files_loaded; pool_index++) {
                    destroy_pool(&preloaded_start_pools[pool_index]);
                }
            }

            free(preloaded_start_pools);
        } else {
            // for now, we only want to read from stdin if a spec is loaded
            if (load_spec_file && spec_loaded) {

                // if the compile flag was set, we don't want to listen to stdin
                if (!compile_flag) {
                    // if no event files were passed to be preloaded, and the compile flag
                    // wasn't set, then we want to read events from stdin
                    line_number = 0;
                    initialize_pool(&input_pool);
                    initialize_pool(&result_pool);

                    while (fgets(line, MAX_LINE_LENGTH, stdin)) {
                        line_number++;

                        read_success = read_event_from_csv(&input_pool, line, line_number, &name_dict, &key_dict, &val_dict, spec_loaded);

                        if (read_success) {
                            // we're only checking spec loaded because maybe we want to eventually do mining
                            // in this code path, but right now it is a little silly
                            if (spec_loaded) {
                                run_nfer(&spec, &input_pool, &result_pool);
                                output_pool(&result_pool, &name_dict, &key_dict, &val_dict, WRITE_OUTPUT);

                                clear_pool(&result_pool);
                            }
                            // don't add the same interval twice
                            clear_pool(&input_pool);
                        }
                    }
                    if (should_log(LOG_LEVEL_INFO)) {
                        log_pool_use("input", &input_pool);
                        log_pool_use("result", &result_pool);
                        log_dictionary_use("names", &name_dict);
                        log_dictionary_use("keys", &key_dict);
                        log_dictionary_use("values", &val_dict);
                        log_specification_use(&name_dict, &spec);
                    }
                    destroy_pool(&result_pool);
                    destroy_pool(&input_pool);
                }
            }
        }

        if (spec_loaded) {
            destroy_specification(&spec);
        }

        // these were initialized at the beginning of the work section
        destroy_dictionary(&val_dict);
        destroy_dictionary(&key_dict);
        destroy_dictionary(&name_dict);
    }

    // make sure this gets freed at some point
    if (event_files) {
        free(event_filenames);
    }

    return 0;
}



