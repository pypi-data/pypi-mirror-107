/*
 * log.c
 *
 *  Created on: Feb 2, 2017
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

#include <stdio.h>
#include <stdarg.h>

#include "types.h"
#include "log.h"

#ifndef NO_STDIO

static int log_level = DEFAULT_LOG_LEVEL;
static bool log_to_file = false;
static bool output_to_file = false;
static FILE *log_handle = NULL;
static FILE *output_handle = NULL;

void set_log_level(int level) {
    log_level = level;
}
void set_log_file(const char *filename) {
    log_to_file = true;
    log_handle = fopen(filename, "a");
}
void set_output_file(const char *filename) {
    output_to_file = true;
    output_handle = fopen(filename, "a");
}
void stop_logging(void) {
    log_level = LOG_LEVEL_NONE;
    if (log_to_file) {
        fclose(log_handle);
    }
    log_to_file = false;
}
void stop_output(void) {
    if (output_to_file) {
        fclose(output_handle);
    }
    output_to_file = false;
}

void filter_log_msg(int level, const char *message, ...) {
    va_list args;
    va_start(args, message);

    if (level <= log_level) {
        if (log_to_file) {
            vfprintf(log_handle, message, args);
        } else {
            vfprintf(stderr, message, args);
        }
    }

    va_end(args);
}

void log_msg(const char *message, ...) {
    va_list args;
    va_start(args, message);

    if (log_to_file) {
        vfprintf(log_handle, message, args);
    } else {
        vfprintf(stderr, message, args);
    }

    va_end(args);
}

bool should_log(int level) {
    return level <= log_level;
}

void write_msg(int log_to, const char *message, ...) {
    va_list args;

    va_start(args, message);
    if (log_to == WRITE_OUTPUT) {
        if (output_to_file) {
            vfprintf(output_handle, message, args);
        } else {
            vfprintf(stdout, message, args);
        }
    } else if (log_to == WRITE_LOGGING) {
        if (log_to_file) {
            vfprintf(log_handle, message, args);
        } else {
            vfprintf(stderr, message, args);
        }
    } else {
        fprintf(stderr, "WENT WRONG: %d\n", log_to);
    }
    // right now, just fail to not writing anything
    va_end(args);
}

#endif
