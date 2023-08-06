/*
 * test_learn.c
 *
 *  Created on: Jan 26, 2017
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

#include <string.h>
#include <stdio.h>

#include "test.h"
#include "test_learn.h"
#include "learn.h"

extern nfer_operator operators[];

static learning learn;
static dictionary dict;

static char *words[] = {
        "foo", "bar", "cat", "dog"
};
#define N_WORDS 4

static interval intervals[] = {
        {0, 0, 0},
        {1, 1, 1},
        {2, 2, 2},
        {3, 3, 3},
        {2, 4, 4},
        {0, 5, 5},
        {1, 6, 6},
        {3, 7, 7},
        {2, 8, 8}
};
#define N_INTS 9

static void setup(void) {
    int i;
    initialize_dictionary(&dict);
    for (i = 0; i < N_WORDS; i++) {
        add_word(&dict, words[i]);
    }
    initialize_learning(&learn, dict.size);
}

static void teardown(void) {
    destroy_learning(&learn);
    destroy_dictionary(&dict);
}

void test_initialize_learning(void) {
    int i;
    setup();

    assert_int_equals("size wrong", 4, learn.size);
    assert_not_null("matrix not initialized", learn.matrix);
    for (i = 0; i < learn.size * learn.size * sizeof(learning_cell); i++) {
        assert_int_equals("matrix not cleared", 0, *((char *) learn.matrix + i));
    }
    assert_not_null("stats not initialized", learn.stats);
    for (i = 0; i < learn.size * sizeof(interval_stat); i++) {
        assert_int_equals("stats not cleared", 0, *((char *) learn.stats + i));
    }

    teardown();
}
void test_destroy_learning(void) {
    setup();
    teardown();

    assert_int_equals("size wrong", 0, learn.size);
    assert_null("matrix not null", learn.matrix);
    assert_null("stats not null", learn.stats);
}
void test_add_learned_rules(void) {
    nfer_specification spec;
    nfer_rule *rule;

    setup();
    initialize_specification(&spec, N_WORDS);

    learn.matrix[0 * learn.size + 1].matches[BEFORE_OPERATOR].success = 3;

    learn.matrix[3 * learn.size + 2].matches[OVERLAP_OPERATOR].success = 2;
    learn.matrix[3 * learn.size + 2].matches[OVERLAP_OPERATOR].failure = 1;

    learn.matrix[2 * learn.size + 0].matches[START_OPERATOR].success = 64;

    add_learned_rules(&learn, &dict, &spec, 1.0, 0.0);

    // check that the dictionary has had 2 words added
    assert_int_equals("two words should have been added", N_WORDS + 2, dict.size);
    assert_str_equals("first added word wrong", "fooBEFbar", dict.words[dict.size - 2].string);
    assert_str_equals("second added word wrong", "catSTfoo", dict.words[dict.size - 1].string);

    // now check that rules were added to the spec
    assert_int_equals("two rules should have been added", 2, spec.rule_list.size);
    // check the first rule
    rule = &spec.rule_list.rules[0];
    assert_int_equals("left label wrong", 0, rule->left_label);
    assert_int_equals("right label wrong", 1, rule->right_label);
    assert_int_equals("result label wrong", 4, rule->result_label);
    assert_ptr_equals("operator wrong", &operators[BEFORE_OPERATOR], rule->op);
    // check the second rule
    rule = &spec.rule_list.rules[1];
    assert_int_equals("left label wrong", 2, rule->left_label);
    assert_int_equals("right label wrong", 0, rule->right_label);
    assert_int_equals("result label wrong", 5, rule->result_label);
    assert_ptr_equals("operator wrong", &operators[START_OPERATOR], rule->op);

    destroy_specification(&spec);
    teardown();
}
void test_finish_learning(void) {
    int i, j, op;
    match *m;

    setup();

    // set up test
    learn.matrix[0 * learn.size + 1].matches[BEFORE_OPERATOR].matched = true;

    learn.matrix[3 * learn.size + 2].matches[OVERLAP_OPERATOR].matched = true;
    learn.matrix[3 * learn.size + 2].matches[OVERLAP_OPERATOR].success = 2;
    learn.matrix[3 * learn.size + 2].matches[OVERLAP_OPERATOR].failure = 1;

    learn.matrix[2 * learn.size + 0].matches[START_OPERATOR].matched = true;
    learn.matrix[2 * learn.size + 0].matches[START_OPERATOR].success = 64;

    learn.matrix[1 * learn.size + 1].matches[FINISH_OPERATOR].failure = 127;
    learn.matrix[2 * learn.size + 2].matches[SLICE_OPERATOR].success = 42;

    // actually call the function
    finish_learning(&learn);

    for (i = 0; i < N_WORDS; i++) {
        for (j = 0; j < N_WORDS; j++) {
            for (op = 0; op < N_OPERATORS; op++) {
                m = &learn.matrix[i * learn.size + j].matches[op];
                if (i == 0 && j == 1 && op == BEFORE_OPERATOR) {
                    assert_int_equals("should have succeeded", 1, m->success);
                    assert_int_equals("should not have failed", 0, m->failure);
                } else if (i == 3 && j == 2 && op == OVERLAP_OPERATOR) {
                    assert_int_equals("should have succeeded", 3, m->success);
                    assert_int_equals("should not have failed", 1, m->failure);
                } else if (i == 2 && j == 0 && op == START_OPERATOR) {
                    assert_int_equals("should have succeeded", 65, m->success);
                    assert_int_equals("should not have failed", 0, m->failure);
                } else if (i == 1 && j == 1 && op == FINISH_OPERATOR) {
                    assert_int_equals("should not have succeeded", 0, m->success);
                    assert_int_equals("should have failed", 128, m->failure);
                } else if (i == 2 && j == 2 && op == SLICE_OPERATOR) {
                    assert_int_equals("should not have succeeded", 42, m->success);
                    assert_int_equals("should have failed", 1, m->failure);
                } else {
                    assert_int_equals("should not have succeeded", 0, m->success);
                    assert_int_equals("should have failed", 1, m->failure);
                }
                assert_false("Matched should be set to false", m->matched);
            }
        }
    }

    teardown();
}

static void check_matrix(int pos, learning_cell *test_matrix) {
    int left, right, op;
    learning_cell *cell, *test_cell;

    left = intervals[pos].name;

    assert_int_equals("start time wrong", intervals[pos].start, learn.stats[left].start);
    assert_int_equals("end time wrong", intervals[pos].end, learn.stats[left].end);
    assert_int_equals("should be seen", true, learn.stats[left].seen);
    // interval is left side
    for (right = 0; right < N_WORDS; right++) {
        cell = &learn.matrix[left * learn.size + right];
        test_cell = &test_matrix[left * learn.size + right];

        for (op = 0; op < N_OPERATORS; op++) {
            //printf("l(%d) r(%d) o(%d)\n", left, right, op);
            assert_int_equals("matched is wrong", test_cell->matches[op].matched, cell->matches[op].matched);
            assert_int_equals("success is wrong", test_cell->matches[op].success, cell->matches[op].success);
            assert_int_equals("failure is wrong", test_cell->matches[op].failure, cell->matches[op].failure);
        }
    }
    // interval is right side
    right = intervals[pos].name;
    for (left = 0; left < N_WORDS; left++) {
        cell = &learn.matrix[left * learn.size + right];
        test_cell = &test_matrix[left * learn.size + right];

        for (op = 0; op < N_OPERATORS; op++) {
            //printf("l(%d) r(%d) o(%d)\n", left, right, op);
            assert_int_equals("matched is wrong", test_cell->matches[op].matched, cell->matches[op].matched);
            assert_int_equals("success is wrong", test_cell->matches[op].success, cell->matches[op].success);
            assert_int_equals("failure is wrong", test_cell->matches[op].failure, cell->matches[op].failure);
        }
    }
}

void test_learn_interval(void) {
    int i, op;
    learning_cell test_matrix[N_WORDS][N_WORDS];

    // use the same sequence of intervals as we had in test_nfer
    setup();

    // initialize test_matrix
    memset(&test_matrix, 0, N_WORDS * N_WORDS * sizeof(learning_cell));

    // get started by adding the first interval
    learn_interval(&learn, &intervals[0]);
    check_matrix(0, (learning_cell *) test_matrix);

    // with the second interval there are things to check
    learn_interval(&learn, &intervals[1]);
    // 0 -> before
    test_matrix[0][1].matches[BEFORE_OPERATOR].matched = true;
    check_matrix(1, (learning_cell *) test_matrix);

    // third interval
    learn_interval(&learn, &intervals[2]);
    test_matrix[0][2].matches[BEFORE_OPERATOR].matched = true;
    test_matrix[1][2].matches[BEFORE_OPERATOR].matched = true;
    check_matrix(2, (learning_cell *) test_matrix);

    // fourth
    learn_interval(&learn, &intervals[3]);
    test_matrix[0][3].matches[BEFORE_OPERATOR].matched = true;
    test_matrix[1][3].matches[BEFORE_OPERATOR].matched = true;
    test_matrix[2][3].matches[BEFORE_OPERATOR].matched = true;
    check_matrix(3, (learning_cell *) test_matrix);

    // with the fifth interval we finally see a duplicate
    learn_interval(&learn, &intervals[4]);
    // just set everything with 2 op X to fail, then change
    // the cells that aren't failures
    for (i = 0; i < N_WORDS; i++) {
        for (op = 0; op < N_OPERATORS; op++) {
            test_matrix[2][i].matches[op].matched = false;
            test_matrix[2][i].matches[op].failure = 1;
        }
    }
    test_matrix[2][2].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[2][2].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[2][3].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[2][3].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[3][2].matches[BEFORE_OPERATOR].matched = true;
    check_matrix(4, (learning_cell *) test_matrix);

    // with the sixth it just gets harder
    learn_interval(&learn, &intervals[5]);
    // do the same thing again
    for (i = 0; i < N_WORDS; i++) {
        for (op = 0; op < N_OPERATORS; op++) {
            test_matrix[0][i].matches[op].matched = false;
            test_matrix[0][i].matches[op].failure = 1;
        }
    }
    test_matrix[0][0].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[0][0].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][1].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[0][1].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][1].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[0][1].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][2].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[0][2].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][3].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[0][3].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[1][0].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[2][0].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[3][0].matches[BEFORE_OPERATOR].matched = 1;
    check_matrix(5, (learning_cell *) test_matrix);

    // seventh
    learn_interval(&learn, &intervals[6]);
    // do the same thing again
    for (i = 0; i < N_WORDS; i++) {
        for (op = 0; op < N_OPERATORS; op++) {
            test_matrix[1][i].matches[op].matched = false;
            test_matrix[1][i].matches[op].failure = 1;
        }
    }
    test_matrix[1][0].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[1][0].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[1][1].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[1][1].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[1][2].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[1][2].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[1][3].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[1][3].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][1].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[2][1].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[3][1].matches[BEFORE_OPERATOR].matched = 1;
    check_matrix(6, (learning_cell *) test_matrix);

    // eighth
    learn_interval(&learn, &intervals[7]);
    // do the same thing again
    for (i = 0; i < N_WORDS; i++) {
        for (op = 0; op < N_OPERATORS; op++) {
            test_matrix[3][i].matches[op].matched = false;
            test_matrix[3][i].matches[op].failure = 1;
        }
    }
    test_matrix[3][0].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[3][0].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[3][1].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[3][1].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[3][2].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[3][2].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[3][3].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[3][3].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][3].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[1][3].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[2][3].matches[BEFORE_OPERATOR].matched = 1;
    check_matrix(7, (learning_cell *) test_matrix);

    // ninth (3rd 2)
    learn_interval(&learn, &intervals[8]);
    // do the same thing again
    for (i = 0; i < N_WORDS; i++) {
        for (op = 0; op < N_OPERATORS; op++) {
            test_matrix[2][i].matches[op].matched = false;
            test_matrix[2][i].matches[op].failure = 2;
        }
    }
    test_matrix[2][0].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[2][0].matches[BEFORE_OPERATOR].failure = 1;
    test_matrix[2][1].matches[BEFORE_OPERATOR].success = 1;
    test_matrix[2][1].matches[BEFORE_OPERATOR].failure = 1;
    test_matrix[2][2].matches[BEFORE_OPERATOR].success = 2;
    test_matrix[2][2].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[2][3].matches[BEFORE_OPERATOR].success = 2;
    test_matrix[2][3].matches[BEFORE_OPERATOR].failure = 0;
    test_matrix[0][2].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[1][2].matches[BEFORE_OPERATOR].matched = 1;
    test_matrix[3][2].matches[BEFORE_OPERATOR].matched = 1;
    check_matrix(8, (learning_cell *) test_matrix);

    teardown();
}
