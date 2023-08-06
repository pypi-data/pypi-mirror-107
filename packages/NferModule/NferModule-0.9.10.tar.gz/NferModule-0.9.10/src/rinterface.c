/*
 * rinterface.c
 *
 *  Created on: Feb 5, 2017
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

#include <R.h>
#include <Rinternals.h>
#include <Rdefines.h>

#include <stdio.h>

#include "types.h"
#include "dict.h"
#include "pool.h"
#include "nfer.h"
#include "log.h"
#include "dsl.h"

#include "learn.h"

#define ROW_NAME_BUFFER_LENGTH 32

/**
 * For the purposes of the R interface, we will just keep singleton dictionaries and spec.
 */

static dictionary name_dict, key_dict, val_dict;
static nfer_specification spec;

static void dataframe_to_pool(SEXP events, pool *p, dictionary *d, bool filter) {
    int i;
    timestamp time_value;
    const char *name_value;
    SEXP names_in, times_in;
    word_id name_id;
    interval *intv;

    // input validation is already done
    names_in = VECTOR_ELT(events, 0);
    times_in = VECTOR_ELT(events, 1);

    for (i = 0; i < length(names_in); i++) {
        // get the strings, which requires first getting the CHARSXP
        name_value = CHAR(STRING_ELT(names_in, i));

        // round the floating point time stamp to the nearest int
        time_value = (timestamp) (REAL(times_in)[i] + 0.5);

        // filter says only add events that are already in the dictionary
        if (!filter || find_word(d, name_value) != WORD_NOT_FOUND) {
            // add to the dictionary (safe even if filter is true)
            name_id = add_word(d, name_value);
            // add to the pool (no map support yet)
            intv = allocate_interval(p);
            intv->name = name_id;
            intv->start = time_value;
            intv->end = time_value;
            intv->hidden = false;
        }
    }
    // make sure the pool is in order
    sort_pool(p);
}

static void pool_to_dataframe(pool *p, dictionary *d, SEXP df) {
    int i, n;
    pool_iterator pit;
    interval *intv;
    SEXP names_out, start_out, end_out;
    SEXP df_class, col_names, row_names;
    char row_name_buffer[ROW_NAME_BUFFER_LENGTH], *result_name;

    // number of results
    n = p->size;

    // allocate the output vectors
    names_out = PROTECT(NEW_CHARACTER(n));
    start_out = PROTECT(NEW_NUMERIC(n));
    end_out = PROTECT(NEW_NUMERIC(n));

    // set up objects to turn out into a data frame
    df_class = PROTECT(mkString("data.frame"));
    row_names = PROTECT(NEW_CHARACTER(n));
    col_names = PROTECT(NEW_CHARACTER(3));
    SET_STRING_ELT(col_names, 0, mkChar("name"));
    SET_STRING_ELT(col_names, 1, mkChar("start"));
    SET_STRING_ELT(col_names, 2, mkChar("end"));

    get_pool_iterator(p, &pit);
    i = 0;
    while (has_next_interval(&pit)) {
        intv = next_interval(&pit);

        // set the name string in the output
        result_name = get_word(d, intv->name);
        SET_STRING_ELT(names_out, i, mkChar(result_name));

        // set the timestamps in the output
        REAL(start_out)[i] = (double) intv->start;
        REAL(end_out)[i] = (double) intv->end;

        // set a row name for the data frame dimension
        sprintf(row_name_buffer, "%d", i);
        SET_STRING_ELT(row_names, i, mkChar(row_name_buffer));
        i++;
    }

    // set names
    SET_VECTOR_ELT(df, 0, names_out);
    // set start times
    SET_VECTOR_ELT(df, 1, start_out);
    // set end times
    SET_VECTOR_ELT(df, 2, end_out);

    // turn it into a data frame
    SET_CLASS(df, df_class);
    SET_NAMES(df, col_names);
    // there's no SET_ROWNAMES
    SET_ATTR(df, R_RowNamesSymbol, row_names);

    UNPROTECT(6);
}

static void load_from_R_handle(SEXP handle,
        nfer_specification **spec,
        dictionary **name_dict,
        dictionary **key_dict,
        dictionary **val_dict) {

    SEXP logfile_vector, loglevel_vector;
    const char *logfile_value;
    int loglevel_value;

    // get the logging values into C variables
    logfile_vector  = VECTOR_ELT(handle, 0);
    loglevel_vector = VECTOR_ELT(handle, 1);

    // set up logging
    logfile_value  = CHAR(STRING_ELT(logfile_vector, 0));
    loglevel_value = INTEGER(loglevel_vector)[0];

    // set the log level and file
    set_log_level(loglevel_value);
    set_log_file(logfile_value);

    // now get the handles from the attributes
    *spec = R_ExternalPtrAddr(getAttrib(handle, install("spec")));
    *name_dict = R_ExternalPtrAddr(getAttrib(handle, install("name_dict")));
    *key_dict = R_ExternalPtrAddr(getAttrib(handle, install("key_dict")));
    *val_dict = R_ExternalPtrAddr(getAttrib(handle, install("val_dict")));
}

static void spec_finalizer(SEXP pointer) {
    if(!R_ExternalPtrAddr(pointer)) {
        return;
    }
    destroy_specification(R_ExternalPtrAddr(pointer));
    R_ClearExternalPtr(pointer);
}

static void dict_finalizer(SEXP pointer) {
    if(!R_ExternalPtrAddr(pointer)) {
        return;
    }
    destroy_dictionary(R_ExternalPtrAddr(pointer));
    R_ClearExternalPtr(pointer);
}

static SEXP initialize_R_nfer(SEXP logfile, SEXP loglevel,
        nfer_specification *spec,
        dictionary *name_dict,
        dictionary *key_dict,
        dictionary *val_dict) {

    SEXP handle, column_names, logfile_handle, loglevel_handle,
         spec_handle, name_dict_handle, key_dict_handle, val_dict_handle;

    const char *logfile_value;
    int loglevel_value;

    // get the parameter values into C variables
    logfile_value  = CHAR(STRING_ELT(logfile, 0));
    loglevel_value = INTEGER_VALUE(loglevel);

    // set the log level and file
    set_log_level(loglevel_value);
    set_log_file(logfile_value);

    // initialize our data structures
    initialize_dictionary(name_dict);
    initialize_dictionary(key_dict);
    initialize_dictionary(val_dict);
    initialize_specification(spec, 0);

    // create a vector to return that has spots for the configuration details
    handle = PROTECT(NEW_LIST(2));

    // create R objects to store the values we want
    logfile_handle = PROTECT(NEW_CHARACTER(1));
    SET_STRING_ELT(logfile_handle, 0, mkChar(logfile_value));
    loglevel_handle = PROTECT(NEW_INTEGER(1));
    INTEGER(loglevel_handle)[0] = loglevel_value;
    column_names = PROTECT(NEW_CHARACTER(2));
    SET_STRING_ELT(column_names, 0, mkChar("logfile"));
    SET_STRING_ELT(column_names, 1, mkChar("loglevel"));

    SET_VECTOR_ELT(handle, 0, logfile_handle);
    SET_VECTOR_ELT(handle, 1, loglevel_handle);
    SET_NAMES(handle, column_names);

    // set up R external pointers for all our data structures
    spec_handle = PROTECT(R_MakeExternalPtr(spec, install("spec"), R_NilValue));
    R_RegisterCFinalizerEx(spec_handle, spec_finalizer, TRUE);
    name_dict_handle = PROTECT(R_MakeExternalPtr(name_dict, install("name_dict"), R_NilValue));
    R_RegisterCFinalizerEx(name_dict_handle, dict_finalizer, TRUE);
    key_dict_handle = PROTECT(R_MakeExternalPtr(key_dict, install("key_dict"), R_NilValue));
    R_RegisterCFinalizerEx(key_dict_handle, dict_finalizer, TRUE);
    val_dict_handle = PROTECT(R_MakeExternalPtr(val_dict, install("val_dict"), R_NilValue));
    R_RegisterCFinalizerEx(val_dict_handle, dict_finalizer, TRUE);

    // add attributes to the handle
    setAttrib(handle, install("spec"), spec_handle);
    setAttrib(handle, install("name_dict"), name_dict_handle);
    setAttrib(handle, install("key_dict"), key_dict_handle);
    setAttrib(handle, install("val_dict"), val_dict_handle);

    UNPROTECT(8);

    return handle;
}

SEXP R_nfer(SEXP specfile, SEXP logfile, SEXP loglevel) {
    SEXP handle;

    const char *specfile_value;

    handle = initialize_R_nfer(logfile, loglevel,
            &spec, &name_dict, &key_dict, &val_dict);

    // get the parameter values into C variables
    specfile_value = CHAR(STRING_ELT(specfile, 0));

    // try to load the spec from the passed file
    load_specification(specfile_value, &spec, &name_dict, &key_dict, &val_dict);

    // teardown logging
    stop_logging();

    return handle;
}

SEXP R_nfer_apply(SEXP handle, SEXP events) {
    SEXP out;

    pool in_pool, out_pool;
    nfer_specification *spec;
    dictionary *name_dict, *key_dict, *val_dict;

    // get the spec, etc. from the passed-in handle
    load_from_R_handle(handle, &spec, &name_dict, &key_dict, &val_dict);

    // initialize the pools
    initialize_pool(&in_pool);
    initialize_pool(&out_pool);

    filter_log_msg(LOG_LEVEL_STATUS, "Creating initial pool\n");
    // get the events from the input
    dataframe_to_pool(events, &in_pool, name_dict, true);
    if (should_log(LOG_LEVEL_DEBUG)) {
        log_msg("\nInitial pool:\n---------------------------\n");
        output_pool(&in_pool, name_dict, key_dict, val_dict, WRITE_LOGGING);
    }

    // resize the specification for all the new symbols
    resize_specification(spec, name_dict->size);

    filter_log_msg(LOG_LEVEL_STATUS, "Applying the rules\n");

    // run the spec on the input events
    run_nfer(spec, &in_pool, &out_pool);

    if (should_log(LOG_LEVEL_INFO)) {
        log_msg("\nResulting pool:\n---------------------------\n");
        output_pool(&out_pool, name_dict, NULL, NULL, WRITE_LOGGING);
    }

    out = PROTECT(NEW_LIST(3));

    filter_log_msg(LOG_LEVEL_STATUS, "Converting pool to dataframe\n");
    pool_to_dataframe(&out_pool, name_dict, out);

    // tear down the nfer objects used
    destroy_pool(&in_pool);
    destroy_pool(&out_pool);

    // tear down logging
    stop_logging();
    stop_output();

    UNPROTECT(1);

    return out;
}

SEXP R_nfer_learn(SEXP events, SEXP logfile, SEXP loglevel) {
    SEXP handle;

    pool in_pool;

    handle = initialize_R_nfer(logfile, loglevel,
            &spec, &name_dict, &key_dict, &val_dict);

    // initialize the input pool
    initialize_pool(&in_pool);

    // get the events and put them into a pool
    dataframe_to_pool(events, &in_pool, &name_dict, false);

    initialize_specification(&spec, name_dict.size);

    // run the learner
    run_learner_on_pool(&in_pool, 1, &name_dict, &key_dict, &val_dict, &spec, DEFAULT_CONFIDENCE, DEFAULT_SUPPORT);

    // tear down the objects used for learning
    destroy_pool(&in_pool);

    // teardown logging
    stop_logging();

    return handle;
}
