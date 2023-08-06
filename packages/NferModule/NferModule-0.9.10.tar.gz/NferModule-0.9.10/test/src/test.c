/*
 * test.c
 *
 *  Created on: Apr 5, 2012
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
#include <string.h>

#include "types.h"
#include "test.h"

// test headers
#include "test_dict.h"
#include "test_pool.h"
#include "test_map.h"
#include "test_stack.h"
#include "test_nfer.h"
//#include "test_learn.h"
#include "test_expression.h"
#include "test_memory.h"
#include "test_strings.h"
#include "test_semantic.h"

// importantly, this file must include headers for all tests

/**
 * The results for all tests.
 */
static int run;
static int passed;
static int failed;
static int asserts_for_test;

/**
 * Runs a series of tests to verify that the program is working properly.
 * Reports on success or failure to the console.  Halts execution if
 * failures are detected.
 *
 *
 * @example run_tests();
 */
int main(void) {
    printf("|----------------------------------------------------------|\n");
    printf("| Running Test Suite                                       |\n");
    printf("|----------------------------------------------------------|\n");

    // test_dictionary
    test_runner(test_initialize_dictionary, "test_initialize_dictionary");
    test_runner(test_destroy_dictionary, "test_destroy_dictionary");
    test_runner(test_add_word, "test_add_word");
    test_runner(test_get_word, "test_get_word");
    // test_pool
    test_runner(test_initialize_pool, "test_initialize_pool");
    test_runner(test_destroy_pool, "test_destroy_pool");
    test_runner(test_add_interval, "test_add_interval");
    test_runner(test_copy_pool, "test_copy_pool");
    test_runner(test_sort_pool, "test_sort_pool");
    test_runner(test_large_ts_sort, "test_large_ts_sort");
    test_runner(test_pool_iterator, "test_pool_iterator");
    test_runner(test_purge_pool, "test_purge_pool");
    // test_map
    test_runner(test_initialize_map, "test_initialize_map");
    test_runner(test_destroy_map, "test_destroy_map");
    test_runner(test_map_set, "test_map_set");
    test_runner(test_map_get, "test_map_get");
    test_runner(test_map_find, "test_map_find");
    // test_stack
    test_runner(test_initialize_stack, "test_initialize_stack");
    test_runner(test_destroy_stack, "test_destroy_stack");
    test_runner(test_push, "test_push");
    test_runner(test_pop, "test_pop");
    // test_nfer
    test_runner(test_initialize_specification, "test_initialize_specification");
    test_runner(test_resize_specification, "test_resize_specification");
    test_runner(test_destroy_specification, "test_destroy_specification");
    test_runner(test_add_rule_to_specification, "test_add_rule_to_specification");
    test_runner(test_add_interval_to_specification, "test_add_interval_to_specification");
    test_runner(test_run_nfer, "test_run_nfer");
    test_runner(test_minimality, "test_minimality");
    test_runner(test_sspss_intervals, "test_sspss_intervals");
    test_runner(test_prolog_intervals, "test_prolog_intervals");
    test_runner(test_beaglebone_intervals, "test_beaglebone_intervals");
    test_runner(test_nfer_dsl, "test_nfer_dsl");
    // test_learn (adding a comment...)
//    test_runner(test_initialize_learning, "test_initialize_learning");
//    test_runner(test_destroy_learning, "test_destroy_learning");
//    test_runner(test_add_learned_rules, "test_add_learned_rules");
//    test_runner(test_finish_learning, "test_finish_learning");
//    test_runner(test_learn_interval, "test_learn_interval");
    // test_expression
    test_runner(test_expression_from_input, "test_expression_from_input");
    test_runner(test_expression_from_runtime, "test_expression_from_runtime");
    // test_memory
    test_runner(test_set_memory, "test_set_memory");
    test_runner(test_clear_memory, "test_clear_memory");
    test_runner(test_copy_memory, "test_copy_memory");
    // test_strings
    test_runner(test_copy_string, "test_copy_string");
    test_runner(test_string_equals, "test_string_equals");
    test_runner(test_string_length, "test_string_length");
    test_runner(test_string_to_u64, "test_string_to_u64");
    test_runner(test_string_to_i64, "test_string_to_i64");
    test_runner(test_string_to_double, "test_string_to_double");
    // test_semantic
    test_runner(test_set_field_mapping_per_rule, "test_set_field_mapping_per_rule");
    test_runner(test_set_time_mapping_per_rule, "test_set_time_mapping_per_rule");
    test_runner(test_remap_field_or_time_mappings, "test_remap_field_or_time_mappings");
    test_runner(test_expr_references_ie, "test_expr_references_bie");
    test_runner(test_remap_nested_boolean, "test_remap_nested_boolean");
    test_runner(test_remap_field_complex, "test_remap_field_complex");
    test_runner(test_set_map_boolean_type, "test_set_map_boolean_type");

    printf("|----------------------------------------------------------|\n");
    printf("| Run:\t\t%d\n| Passed:\t%d\n| Failed:\t%d\n", run, passed, failed);
    printf("|----------------------------------------------------------|\n");

    return failed;
}

void test_runner(void (*test)(void), const char *name) {
    int startRun;
    int startFailed;

    // init assertions for this test
    asserts_for_test = 0;

    // get the starting values of run and failed
    startRun = run;
    startFailed = failed;

    // print the test name, so it is clear what failed if there is an error
    printf("  Test: %34s\t", name);

    // run the test
    test();

    // compare the values and print a message about the success or failure
    if (run <= startRun) {
        printf("\033[33m[SKIP]\033[0m\n");
    } else if (failed == startFailed) {
        printf("\033[32m[PASS]\033[0m\n");
    } else {
        printf("\033[1;31m[FAIL]\033[0m\n");
    }
}

static bool assert(char *msg, bool val, char *expected, char *found) {
    asserts_for_test = asserts_for_test + 1;

    if (val) {
        passed = passed + 1;
    } else {
        failed = failed + 1;
        printf("Failure (%d): %s\nExpected <%s> but was <%s>\n", asserts_for_test,
                msg, expected, found);
    }

    run = run + 1;
    return val;
}

void assert_true(char *msg, bool val) {
    assert(msg, val, "true", "false");
}

void assert_false(char *msg, bool val) {
    assert(msg, !val, "false", "true");
}

void assert_null(char *msg, void *val) {
    assert(msg, (val == NULL ), "null", "not null");
}

void assert_not_null(char *msg, void *val) {
    assert(msg, (val != NULL ), "not null", "null");
}

void assert_str_equals(char *msg, char *val0, char *val1) {
    assert(msg, (strcmp(val0, val1) == 0), val0, val1);
}

void assert_int_equals(char *msg, unsigned long long val0, unsigned long long val1) {
    /* 20 chars max, plus 1 for null terminator */
    char buf0[21];
    char buf1[21];
    sprintf(&buf0[0], "%llu", val0);
    sprintf(&buf1[0], "%llu", val1);

    assert(msg, (val0 == val1), buf0, buf1);
}

void assert_ptr_equals(char *msg, void *val0, void *val1) {
    /* 18 chars max, plus 2 for the 0x, plus 1 for null terminator */
    char buf0[21];
    char buf1[21];
    sprintf(&buf0[0], "%p", val0);
    sprintf(&buf1[0], "%p", val1);

    assert(msg, (val0 == val1), buf0, buf1);
}

void assert_float_equals(char *msg, double val0, double val1) {
    // more or less equals...
    const double epsilon = 0.00000001;
    /* 20 chars max, plus 2 for 0. maybe?, plus 1 for null terminator */
    char buf0[23];
    char buf1[23];
    sprintf(&buf0[0], "%20f", val0);
    sprintf(&buf1[0], "%20f", val1);

    assert(msg, ((val0 >= val1 - epsilon) && (val0 <= val1 + epsilon)), buf0, buf1);
}

