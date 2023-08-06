/*
 * test_nfer.c
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

#include <stdio.h>

#include "test.h"
#include "test_nfer.h"
#include "nfer.h"
#include "pool.h"
#include "log.h"

static nfer_specification spec;

#define INITIAL_SPEC_SIZE 0

static void setup(void) {
    initialize_specification(&spec, INITIAL_SPEC_SIZE);
}

static void teardown(void) {
    destroy_specification(&spec);
}

void test_initialize_specification(void) {
    unsigned int i;
    setup();

    // because size was 0 in init call
    assert_int_equals("subscription_size wrong", 0, spec.subscription_size);
    assert_null("left_subscriptions wrong", spec.subscriptions[LEFT_SUBSCRIPTIONS]);
    assert_null("right_subscriptions wrong", spec.subscriptions[RIGHT_SUBSCRIPTIONS]);

    assert_int_equals("rule_list.space wrong", INITIAL_RULE_LIST_LENGTH, spec.rule_list.space);
    assert_int_equals("rule_list.size wrong", 0, spec.rule_list.size);
    assert_not_null("rule_list.rules null", spec.rule_list.rules);

    for (i = 0; i < spec.rule_list.space * sizeof(nfer_rule); i++) {
        assert_int_equals("rules not cleared", 0, *((char *) spec.rule_list.rules + i));
    }

    teardown();
}
void test_resize_specification(void) {
    unsigned int i, side;
    setup();

    // first allocation
    resize_specification(&spec, 4);
    assert_int_equals("subscription_size wrong", 4, spec.subscription_size);
    assert_not_null("left_subscriptions wrong", spec.subscriptions[LEFT_SUBSCRIPTIONS]);
    assert_not_null("right_subscriptions wrong", spec.subscriptions[RIGHT_SUBSCRIPTIONS]);

    // test cleared
    for (side = 0; side < N_SUBSCRIPTION_LISTS; side++) {
        for (i = 0; i < spec.subscription_size * sizeof(rule_id); i++) {
            assert_int_equals("subscriptions not set", (char)-1, *((char *) spec.subscriptions[side] + i));
        }
    }

    // add some dummy values
    spec.subscriptions[LEFT_SUBSCRIPTIONS][0] = 0xffff;
    spec.subscriptions[LEFT_SUBSCRIPTIONS][2] = 0x1234;
    spec.subscriptions[RIGHT_SUBSCRIPTIONS][3] = 0xeeee;
    spec.subscriptions[RIGHT_SUBSCRIPTIONS][1] = 0x4321;

    // resize it
    resize_specification(&spec, 8);
    assert_int_equals("subscription_size wrong", 8, spec.subscription_size);
    assert_not_null("left_subscriptions wrong", spec.subscriptions[LEFT_SUBSCRIPTIONS]);
    assert_not_null("right_subscriptions wrong", spec.subscriptions[RIGHT_SUBSCRIPTIONS]);

    // test new values cleared
    for (side = 0; side < N_SUBSCRIPTION_LISTS; side++) {
        for (i = 4 * sizeof(rule_id); i < spec.subscription_size * sizeof(rule_id); i++) {
            assert_int_equals("subscriptions not set", (char)-1, *((char *) spec.subscriptions[side] + i));
        }
    }

    // check that the old values are still there
    assert_int_equals("dummy subscription removed", 0xffff, (int) spec.subscriptions[LEFT_SUBSCRIPTIONS][0]);
    assert_int_equals("dummy subscription removed", 0x1234, (int) spec.subscriptions[LEFT_SUBSCRIPTIONS][2]);
    assert_int_equals("dummy subscription removed", 0xeeee, (int) spec.subscriptions[RIGHT_SUBSCRIPTIONS][3]);
    assert_int_equals("dummy subscription removed", 0x4321, (int) spec.subscriptions[RIGHT_SUBSCRIPTIONS][1]);

    teardown();
}
void test_destroy_specification(void) {
    setup();

    // consider adding some rules here, to make sure they are properly deallocated

    resize_specification(&spec, 4);

    teardown();

    assert_int_equals("subscription_size wrong", 0, spec.subscription_size);
    assert_null("left_subscriptions wrong", spec.subscriptions[LEFT_SUBSCRIPTIONS]);
    assert_null("right_subscriptions wrong", spec.subscriptions[RIGHT_SUBSCRIPTIONS]);

    assert_int_equals("rule_list.space wrong", 0, spec.rule_list.space);
    assert_int_equals("rule_list.size wrong", 0, spec.rule_list.size);
    assert_null("rule_list.rules not null", spec.rule_list.rules);
}

// helper functions
static void check_rule_status(nfer_rule *rule, operator_code op_code, label lhs, label rhs, label res, rule_id nextl, rule_id nextr) {
    // check the rule fields
    assert_int_equals("operator is wrong", op_code, rule->op_code);
    assert_int_equals("lhs interval is wrong", lhs, rule->left_label);
    assert_int_equals("rhs interval is wrong", rhs, rule->right_label);
    assert_int_equals("result interval is wrong", res, rule->result_label);
    // check the linked lists
    assert_int_equals("next_left wrong", nextl, rule->next[LEFT_SUBSCRIPTIONS]);
    assert_int_equals("next_right wrong", nextr, rule->next[RIGHT_SUBSCRIPTIONS]);
}

static void check_cache_status(nfer_rule *rule) {
    // check the caches
    assert_int_equals("left cache should be empty", 0, rule->left_cache.size);
    assert_int_equals("left cache should be initialized", INITIAL_POOL_SIZE, rule->left_cache.space);
    assert_int_equals("right cache should be empty", 0, rule->right_cache.size);
    assert_int_equals("right cache should be initialized", INITIAL_POOL_SIZE, rule->right_cache.space);
    assert_int_equals("produced cache should be empty", 0, rule->produced.size);
    assert_int_equals("produced cache should be initialized", INITIAL_POOL_SIZE, rule->produced.space);
}

#define LEFT LEFT_SUBSCRIPTIONS
#define RIGHT RIGHT_SUBSCRIPTIONS
static void check_subscriptions(int side, int i, nfer_rule *one, nfer_rule *two, nfer_rule *three) {
    rule_id index;
    nfer_rule *sub;
    label name;

    index = spec.subscriptions[side][i];

    if (index != MISSING_RULE_ID) {
        sub = &spec.rule_list.rules[index];
        assert_ptr_equals("first subscriber wrong", one, sub);

        name = side ? sub->right_label : sub->left_label;
        assert_int_equals("wrong subscription name", i, name);

        index = sub->next[side];

        if (index != MISSING_RULE_ID) {
            sub = &spec.rule_list.rules[index];
            assert_ptr_equals("second subscriber wrong", two, sub);

            name = side ? sub->right_label : sub->left_label;
            assert_int_equals("wrong subscription name", i, name);

            index = sub->next[side];
            if (index != MISSING_RULE_ID) {
                sub = &spec.rule_list.rules[index];
                assert_ptr_equals("third subscriber wrong", three, sub);

                name = side ? sub->right_label : sub->left_label;
                assert_int_equals("wrong subscription name", i, name);
            }
        }
    }
}

void test_add_rule_to_specification(void) {
    nfer_rule_list *rules;
    nfer_rule *rule1, *rule2, *rule3, *rule4;
    unsigned int i;
    setup();

    resize_specification(&spec, 4);
    rules = &spec.rule_list;

    // add a rule
    add_rule_to_specification(&spec, 1, 1, BEFORE_OPERATOR, 1, NULL);
    // check the rules list
    assert_int_equals("size is wrong", 1, rules->size);
    rule1 = &rules->rules[rules->size - 1];
    check_rule_status(rule1, 1, 1, 1, 1, MISSING_RULE_ID, MISSING_RULE_ID);
    check_cache_status(rule1);
    check_subscriptions(LEFT, 0, NULL, NULL, NULL);
    check_subscriptions(LEFT, 1, rule1, NULL, NULL);
    check_subscriptions(LEFT, 2, NULL, NULL, NULL);
    check_subscriptions(LEFT, 3, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 0, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 1, rule1, NULL, NULL);
    check_subscriptions(RIGHT, 2, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 3, NULL, NULL, NULL);

    // add another rule
    add_rule_to_specification(&spec, 2, 1, MEET_OPERATOR, 2, NULL);
    // check the rules list
    assert_int_equals("size is wrong", 2, rules->size);
    rule2 = &rules->rules[rules->size - 1];
    check_rule_status(rule2, 2, 1, 2, 2, 0, MISSING_RULE_ID);
    check_cache_status(rule2);
    check_subscriptions(LEFT, 0, NULL, NULL, NULL);
    check_subscriptions(LEFT, 1, rule2, rule1, NULL);
    check_subscriptions(LEFT, 2, NULL, NULL, NULL);
    check_subscriptions(LEFT, 3, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 0, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 1, rule1, NULL, NULL);
    check_subscriptions(RIGHT, 2, rule2, NULL, NULL);
    check_subscriptions(RIGHT, 3, NULL, NULL, NULL);

    // add 2 more
    add_rule_to_specification(&spec, 3, 1, DURING_OPERATOR, 3, NULL);
    rule3 = &rules->rules[rules->size - 1];
    check_rule_status(rule3, 3, 1, 3, 3, 1, MISSING_RULE_ID);
    check_cache_status(rule3);
    add_rule_to_specification(&spec, 0, 1, COINCIDE_OPERATOR, 0, NULL);
    rule4 = &rules->rules[rules->size - 1];
    check_rule_status(rule4, 4, 1, 0, 0, 2, MISSING_RULE_ID);
    check_cache_status(rule4);

    // check the rules list
    assert_int_equals("size is wrong", 4, rules->size);
    assert_int_equals("space is wrong", INITIAL_POOL_SIZE, rules->space);

    check_subscriptions(LEFT, 0, NULL, NULL, NULL);
    check_subscriptions(LEFT, 1, rule4, rule3, rule2);
    check_subscriptions(LEFT, 2, NULL, NULL, NULL);
    check_subscriptions(LEFT, 3, NULL, NULL, NULL);
    check_subscriptions(RIGHT, 0, rule4, NULL, NULL);
    check_subscriptions(RIGHT, 1, rule1, NULL, NULL);
    check_subscriptions(RIGHT, 2, rule2, NULL, NULL);
    check_subscriptions(RIGHT, 3, rule3, NULL, NULL);

    // now add intervals until the rules list must be resized
    for (i = 0; i < INITIAL_POOL_SIZE + 1 - 4; i++) {
        add_rule_to_specification(&spec, 1, 1, BEFORE_OPERATOR, 1, NULL);
    }
    assert_int_equals("size is wrong", INITIAL_POOL_SIZE + 1, rules->size);
    assert_int_equals("space is wrong", INITIAL_POOL_SIZE * 2, rules->space);
    assert_int_equals("subscription is wrong", rules->size - 1, spec.subscriptions[LEFT_SUBSCRIPTIONS][1]);

    for (i = (INITIAL_POOL_SIZE + 1) * sizeof(nfer_rule); i < spec.rule_list.space * sizeof(nfer_rule); i++) {
        assert_int_equals("rules not cleared", 0, *((char *) spec.rule_list.rules + i));
    }

    teardown();
}

/*
 * Rules:
 * 4 <- 0 before 2
 * 5 <- 1 before 3
 *
 * 6 <- 4 slice 5
 *
 * Trace:
 * 0 @ 0 -- 4
 * 1 @ 1 ---|-- 5-- 6
 * 2 @ 2 -- 4---|-- 6
 * 3 @ 3 -------5
 * 2 @ 4
 * 0 @ 5 ------ 4
 * 1 @ 6 -- 5---|-- 6
 * 3 @ 7 -- 5---|-- 6
 * 2 @ 8 ------ 4
 */
void test_add_interval_to_specification(void) {
#define N_INTS 9
    interval intervals[] = {
            { 0, 0, 0, EMPTY_MAP, false },
            { 1, 1, 1, EMPTY_MAP, false },
            { 2, 2, 2, EMPTY_MAP, false },
            { 3, 3, 3, EMPTY_MAP, false },
            { 2, 4, 4, EMPTY_MAP, false },
            { 0, 5, 5, EMPTY_MAP, false },
            { 1, 6, 6, EMPTY_MAP, false },
            { 3, 7, 7, EMPTY_MAP, false },
            { 2, 8, 8, EMPTY_MAP, false } };
    pool out1, out2;
    nfer_rule *rule0b2, *rule1b3, *rule4s5;

    setup();
    initialize_pool(&out1);
    initialize_pool(&out2);

    // Phase 1
    resize_specification(&spec, 4);
    add_rule_to_specification(&spec, 4, 0, BEFORE_OPERATOR, 2, NULL); // 4 <- 0 before 2
    add_rule_to_specification(&spec, 5, 1, BEFORE_OPERATOR, 3, NULL); // 5 <- 1 before 3
    // get references for easier checking
    rule0b2 = &spec.rule_list.rules[0];
    rule1b3 = &spec.rule_list.rules[1];

    add_interval_to_specification(&spec, &intervals[0], &out1);
    assert_int_equals("out size wrong", 0, out1.size);
    assert_int_equals("left_size wrong", 1, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 0, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule1b3->right_cache.size);

    add_interval_to_specification(&spec, &intervals[1], &out1);
    assert_int_equals("out size wrong", 0, out1.size);
    assert_int_equals("left_size wrong", 1, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule1b3->right_cache.size);

    add_interval_to_specification(&spec, &intervals[2], &out1);
    assert_int_equals("out size wrong", 1, out1.size);
    assert_int_equals("left_size wrong", 1, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule1b3->right_cache.size);
    assert_int_equals("generated interval name wrong", 4, out1.intervals[0].i.name);
    assert_int_equals("generated interval start wrong", 0, out1.intervals[0].i.start);
    assert_int_equals("generated interval end wrong", 2, out1.intervals[0].i.end);

    add_interval_to_specification(&spec, &intervals[3], &out1);
    assert_int_equals("out size wrong", 2, out1.size);
    assert_int_equals("left_size wrong", 1, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule1b3->right_cache.size);
    assert_int_equals("generated interval name wrong", 5, out1.intervals[1].i.name);
    assert_int_equals("generated interval start wrong", 1, out1.intervals[1].i.start);
    assert_int_equals("generated interval end wrong", 3, out1.intervals[1].i.end);

    add_interval_to_specification(&spec, &intervals[4], &out1);
    assert_int_equals("out size wrong", 2, out1.size);
    assert_int_equals("left_size wrong", 1, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule1b3->right_cache.size);

    add_interval_to_specification(&spec, &intervals[5], &out1);
    assert_int_equals("out size wrong", 2, out1.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule1b3->right_cache.size);

    add_interval_to_specification(&spec, &intervals[6], &out1);
    assert_int_equals("out size wrong", 2, out1.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule1b3->right_cache.size);

    add_interval_to_specification(&spec, &intervals[7], &out1);
    assert_int_equals("out size wrong", 3, out1.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("generated interval name wrong", 5, out1.intervals[2].i.name);
    assert_int_equals("generated interval start wrong", 6, out1.intervals[2].i.start);
    assert_int_equals("generated interval end wrong", 7, out1.intervals[2].i.end);

    add_interval_to_specification(&spec, &intervals[8], &out1);
    assert_int_equals("out size wrong", 4, out1.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 3, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("generated interval name wrong", 4, out1.intervals[3].i.name);
    assert_int_equals("generated interval start wrong", 5, out1.intervals[3].i.start);
    assert_int_equals("generated interval end wrong", 8, out1.intervals[3].i.end);

    // Phase 2
    resize_specification(&spec, 6);
    add_rule_to_specification(&spec, 6, 4, SLICE_OPERATOR, 5, NULL); // 6 <- 4 slice 5
    // get reference for easier checking
    rule4s5 = &spec.rule_list.rules[2];

    add_interval_to_specification(&spec, &out1.intervals[0].i, &out2);
    assert_int_equals("out size wrong", 0, out2.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 3, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule4s5->left_cache.size);
    assert_int_equals("right_size wrong", 0, rule4s5->right_cache.size);

    add_interval_to_specification(&spec, &out1.intervals[1].i, &out2);
    assert_int_equals("out size wrong", 1, out2.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 3, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule4s5->left_cache.size);
    assert_int_equals("right_size wrong", 1, rule4s5->right_cache.size);
    assert_int_equals("generated interval name wrong", 6, out2.intervals[0].i.name);
    assert_int_equals("generated interval start wrong", 1, out2.intervals[0].i.start);
    assert_int_equals("generated interval end wrong", 2, out2.intervals[0].i.end);

    add_interval_to_specification(&spec, &out1.intervals[2].i, &out2);
    assert_int_equals("out size wrong", 1, out2.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 3, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("left_size wrong", 1, rule4s5->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule4s5->right_cache.size);

    add_interval_to_specification(&spec, &out1.intervals[3].i, &out2);
    assert_int_equals("out size wrong", 2, out2.size);
    assert_int_equals("left_size wrong", 2, rule0b2->left_cache.size);
    assert_int_equals("right_size wrong", 3, rule0b2->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule1b3->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule1b3->right_cache.size);
    assert_int_equals("left_size wrong", 2, rule4s5->left_cache.size);
    assert_int_equals("right_size wrong", 2, rule4s5->right_cache.size);
    assert_int_equals("generated interval name wrong", 6, out2.intervals[1].i.name);
    assert_int_equals("generated interval start wrong", 6, out2.intervals[1].i.start);
    assert_int_equals("generated interval end wrong", 7, out2.intervals[1].i.end);

    destroy_pool(&out2);
    destroy_pool(&out1);
    teardown();
}

/*
 * Rules:
 * 4 <- 0 before 2
 * 5 <- 1 before 3
 *
 * 6 <- 4 slice 5
 *
 * Trace:
 * 0 @ 0 -- 4
 * 1 @ 1 ---|-- 5-- 6
 * 2 @ 2 -- 4---|-- 6
 * 3 @ 3 -------5
 * 2 @ 4
 * 0 @ 5 ------ 4
 * 1 @ 6 -- 5---|-- 6
 * 3 @ 7 -- 5---|-- 6
 * 2 @ 8 ------ 4
 */
void test_run_nfer(void) {
#define N_INTS 9
    interval intervals[] = {
            { 0, 0, 0, EMPTY_MAP, false },
            { 1, 1, 1, EMPTY_MAP, false },
            { 2, 2, 2, EMPTY_MAP, false },
            { 3, 3, 3, EMPTY_MAP, false },
            { 2, 4, 4, EMPTY_MAP, false },
            { 0, 5, 5, EMPTY_MAP, false },
            { 1, 6, 6, EMPTY_MAP, false },
            { 3, 7, 7, EMPTY_MAP, false },
            { 2, 8, 8, EMPTY_MAP, false }
    };
    int i;
    pool in, out;
    interval *check;
    pool_iterator pit;

    setup();
    initialize_pool(&in);
    initialize_pool(&out);

    // add the rules
    resize_specification(&spec, 7);
    add_rule_to_specification(&spec, 4, 0, BEFORE_OPERATOR, 2, NULL); // 4 <- 0 before 2
    add_rule_to_specification(&spec, 5, 1, BEFORE_OPERATOR, 3, NULL); // 5 <- 1 before 3
    add_rule_to_specification(&spec, 6, 4, SLICE_OPERATOR, 5, NULL); // 6 <- 4 slice 5

    // add the intervals to the input pool
    for (i = 0; i < N_INTS; i++) {
        add_interval(&in, &intervals[i]);
    }

    // run nfer
    run_nfer(&spec, &in, &out);

    get_pool_iterator(&out, &pit);

    // check the results
    assert_int_equals("input size wrong", N_INTS, in.size);
    assert_int_equals("output size wrong", 6, out.size);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 4, check->name);
    assert_int_equals("generated interval start wrong", 0, check->start);
    assert_int_equals("generated interval end wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 6, check->name);
    assert_int_equals("generated interval start wrong", 1, check->start);
    assert_int_equals("generated interval end wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 5, check->name);
    assert_int_equals("generated interval start wrong", 1, check->start);
    assert_int_equals("generated interval end wrong", 3, check->end);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 5, check->name);
    assert_int_equals("generated interval start wrong", 6, check->start);
    assert_int_equals("generated interval end wrong", 7, check->end);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 6, check->name);
    assert_int_equals("generated interval start wrong", 6, check->start);
    assert_int_equals("generated interval end wrong", 7, check->end);

    check = next_interval(&pit);
    assert_int_equals("generated interval name wrong", 4, check->name);
    assert_int_equals("generated interval start wrong", 5, check->start);
    assert_int_equals("generated interval end wrong", 8, check->end);

    destroy_pool(&out);
    destroy_pool(&in);
    teardown();
}

void test_minimality(void) {
    interval intervals[] = {
            { 0, 10, 15, EMPTY_MAP, false },
            { 0, 20, 25, EMPTY_MAP, false },
            { 1, 30, 35, EMPTY_MAP, false }
    };
    pool out;

    setup();
    initialize_pool(&out);

    // add the rules
    resize_specification(&spec, 3);
    add_rule_to_specification(&spec, 2, 0, BEFORE_OPERATOR, 1, NULL); // 2 <- 0 before 1

    add_interval_to_specification(&spec, &intervals[0], &out);
    assert_int_equals("No interval should be generated", 0, out.size);

    add_interval_to_specification(&spec, &intervals[1], &out);
    assert_int_equals("No interval should be generated", 0, out.size);

    add_interval_to_specification(&spec, &intervals[2], &out);
    assert_int_equals("One interval should be generated", 1, out.size);

    assert_int_equals("Name wrong", 2, out.intervals[0].i.name);
    assert_int_equals("Start wrong", 20, out.intervals[0].i.start);
    assert_int_equals("End wrong", 35, out.intervals[0].i.end);

    destroy_pool(&out);
    teardown();
}

void test_sspss_intervals(void) {
    label mark1 = 0, mark2 = 1, mark3 = 2, mark4 = 3, mark5 = 4;
    label acquisition = 5, processing1 = 6, processing2wc = 7, processing2to5 = 8, processing2woc = 9, communication =
            10, sleep = 11, processing = 12, handling = 13, finalization = 14, sspss = 15;
    int i;
    interval intervals[] = {
            { mark2, 3570703667UL, 3570703667UL, EMPTY_MAP, false },
            { mark3, 3871719292UL, 3871719292UL, EMPTY_MAP, false },
            { mark4, 26884595250UL, 26884595250UL, EMPTY_MAP, false },
            { mark5, 29364814584UL, 29364814584UL, EMPTY_MAP, false },
            { mark1, 36433289167UL, 36433289167UL, EMPTY_MAP, false },
            { mark2, 45096812209UL, 45096812209UL, EMPTY_MAP, false },
            { mark3, 45406664209UL, 45406664209UL, EMPTY_MAP, false },
//			{mark4, 68212600750UL, 68212600750, EMPTY_MAP}, // remove this because we want to see a non-negation
            { mark5, 70795198750UL, 70795198750UL, EMPTY_MAP, false },
            { mark1, 77865924917UL, 77865924917UL, EMPTY_MAP, false } };

    pool in, out;
    pool_iterator pit;
    interval *check;

    setup();
    initialize_pool(&in);
    initialize_pool(&out);

    // add all the test intervals to the pool
    for (i = 0; i < 9; i++) {
        add_interval(&in, &intervals[i]);
    }

    // add the rules
    resize_specification(&spec, 16);
    add_rule_to_specification(&spec, acquisition, mark1, BEFORE_OPERATOR, mark2, NULL);
    add_rule_to_specification(&spec, processing1, mark2, BEFORE_OPERATOR, mark3, NULL);
    // we need to actually exclude the presence of mark4 from the woc version...
    add_rule_to_specification(&spec, processing2wc, mark3, BEFORE_OPERATOR, mark4, NULL);
    add_rule_to_specification(&spec, processing2to5, mark3, BEFORE_OPERATOR, mark5, NULL);
    // this ensures that we don't get a processing2woc unless comm is missing
    add_rule_to_specification(&spec, processing2woc, processing2to5, CONTAIN_OPERATOR, mark4, NULL);

    add_rule_to_specification(&spec, communication, mark4, BEFORE_OPERATOR, mark5, NULL);
    add_rule_to_specification(&spec, sleep, mark5, BEFORE_OPERATOR, mark1, NULL);

    // disjunction...
    add_rule_to_specification(&spec, processing, processing1, MEET_OPERATOR, processing2wc, NULL);
    add_rule_to_specification(&spec, processing, processing1, MEET_OPERATOR, processing2woc, NULL);

    add_rule_to_specification(&spec, handling, acquisition, MEET_OPERATOR, processing, NULL);
    // more disjunction...
    add_rule_to_specification(&spec, finalization, communication, MEET_OPERATOR, sleep, NULL);
    add_rule_to_specification(&spec, finalization, sleep, FOLLOW_OPERATOR, communication, NULL);

    // wrap it up
    add_rule_to_specification(&spec, sspss, handling, MEET_OPERATOR, finalization, NULL);

    // actually run nfer
    run_nfer(&spec, &in, &out);

    assert_int_equals("size of out is wrong", 16, out.size);

//    get_pool_iterator(&out, &pit);
//    while (has_next_interval(&pit)) {
//        check = next_interval(&pit);
//        log_interval(check);
//    }

    get_pool_iterator(&out, &pit);

    check = next_interval(&pit);
    assert_int_equals("result 1 label is wrong", processing1, check->name);
    assert_int_equals("result 1 start is wrong", intervals[0].start, check->start);
    assert_int_equals("result 1 end is wrong", intervals[1].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 2 label is wrong", processing, check->name);
    assert_int_equals("result 2 start is wrong", intervals[0].start, check->start);
    assert_int_equals("result 2 end is wrong", intervals[2].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 3 label is wrong", processing2wc, check->name);
    assert_int_equals("result 3 start is wrong", intervals[1].start, check->start);
    assert_int_equals("result 3 end is wrong", intervals[2].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 4 label is wrong", processing2to5, check->name);
    assert_int_equals("result 4 start is wrong", intervals[1].start, check->start);
    assert_int_equals("result 4 end is wrong", intervals[3].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 5 label is wrong", communication, check->name);
    assert_int_equals("result 5 start is wrong", intervals[2].start, check->start);
    assert_int_equals("result 5 end is wrong", intervals[3].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 6 label is wrong", finalization, check->name);
    assert_int_equals("result 6 start is wrong", intervals[2].start, check->start);
    assert_int_equals("result 6 end is wrong", intervals[4].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 7 label is wrong", sleep, check->name);
    assert_int_equals("result 7 start is wrong", intervals[3].start, check->start);
    assert_int_equals("result 7 end is wrong", intervals[4].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 8 label is wrong", acquisition, check->name);
    assert_int_equals("result 8 start is wrong", intervals[4].start, check->start);
    assert_int_equals("result 8 end is wrong", intervals[5].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 9 label is wrong", processing1, check->name);
    assert_int_equals("result 9 start is wrong", intervals[5].start, check->start);
    assert_int_equals("result 9 end is wrong", intervals[6].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 10 label is wrong", handling, check->name);
    assert_int_equals("result 10 start is wrong", intervals[4].start, check->start);
    assert_int_equals("result 10 end is wrong", intervals[7].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 11 label is wrong", processing, check->name);
    assert_int_equals("result 11 start is wrong", intervals[5].start, check->start);
    assert_int_equals("result 11 end is wrong", intervals[7].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 12 label is wrong", processing2to5, check->name);
    assert_int_equals("result 12 start is wrong", intervals[6].start, check->start);
    assert_int_equals("result 12 end is wrong", intervals[7].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 13 label is wrong", processing2woc, check->name);
    assert_int_equals("result 13 start is wrong", intervals[6].start, check->start);
    assert_int_equals("result 13 end is wrong", intervals[7].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 14 label is wrong", sspss, check->name);
    assert_int_equals("result 14 start is wrong", intervals[4].start, check->start);
    assert_int_equals("result 14 end is wrong", intervals[8].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 15 label is wrong", sleep, check->name);
    assert_int_equals("result 15 start is wrong", intervals[7].start, check->start);
    assert_int_equals("result 15 end is wrong", intervals[8].end, check->end);

    check = next_interval(&pit);
    assert_int_equals("result 16 label is wrong", finalization, check->name);
    assert_int_equals("result 16 start is wrong", intervals[7].start, check->start);
    assert_int_equals("result 16 end is wrong", intervals[8].end, check->end);

    destroy_pool(&out);
    destroy_pool(&in);
    teardown();
}

static bool within300(
        timestamp ls, timestamp UNUSED(le), data_map *UNUSED(left),
        timestamp UNUSED(rs), timestamp re, data_map *UNUSED(right)) {
    return (re - ls) < 300;
}

void test_prolog_intervals(void) {
    //    Adding interval to spec (24,40,46)
    //    Adding interval to spec (24,44,50)
    label boot_s_f = 0, downlink = 1, boot_s_a = 2, boot_s_d = 3,
            boot_e_f = 4, boot_e_d = 5, boot_e_a = 6;
    label boot = 7, dboot = 8, risk = 9;
    interval intervals[] = {
            { boot_s_f, 40, 40, EMPTY_MAP, false },
            { downlink, 41, 41, EMPTY_MAP, false },
            { boot_s_a, 42, 42, EMPTY_MAP, false },
            { boot_s_d, 44, 44, EMPTY_MAP, false },
            { boot_e_f, 46, 46, EMPTY_MAP, false },
            { downlink, 48, 48, EMPTY_MAP, false },
            { boot_e_d, 50, 50, EMPTY_MAP, false }
    };
    pool in, out;
    interval *check;
    int i;
    phi_function within300_phi = { "WITHIN300", within300, NULL };

    setup();
    initialize_pool(&in);
    initialize_pool(&out);

    // add all the test intervals to the pool
    for (i = 0; i < 7; i++) {
        add_interval(&in, &intervals[i]);
    }

    resize_specification(&spec, 10);
    add_rule_to_specification(&spec, boot, boot_s_a, BEFORE_OPERATOR, boot_e_a, NULL);
    add_rule_to_specification(&spec, boot, boot_s_d, BEFORE_OPERATOR, boot_e_d, NULL);
    add_rule_to_specification(&spec, boot, boot_s_f, BEFORE_OPERATOR, boot_e_f, NULL);

    add_rule_to_specification(&spec, dboot, boot, BEFORE_OPERATOR, boot, &within300_phi);
    add_rule_to_specification(&spec, risk, downlink, DURING_OPERATOR, dboot, NULL);

    // actually run nfer
    run_nfer(&spec, &in, &out);

    assert_int_equals("result size is wrong", 2, out.size);
    i = 0;

    check = &out.intervals[i++].i;
    assert_int_equals("result label is wrong", boot, check->name);
    assert_int_equals("result start is wrong", intervals[0].start, check->start);
    assert_int_equals("result end is wrong", intervals[4].end, check->end);

    check = &out.intervals[i++].i;
    assert_int_equals("result label is wrong", boot, check->name);
    assert_int_equals("result start is wrong", intervals[3].start, check->start);
    assert_int_equals("result end is wrong", intervals[6].end, check->end);

    destroy_pool(&out);
    destroy_pool(&in);
    teardown();
}

static bool equal_event_string(
        timestamp UNUSED(ls), timestamp UNUSED(le), data_map *left,
        timestamp UNUSED(rs), timestamp UNUSED(re), data_map *right) {
    map_value left_value, right_value;

    map_get(left, 0, &left_value);
    map_get(right, 0, &right_value);
    if (left_value.type != string_type ||
            right_value.type != string_type) {
        return false;
    }

    return left_value.string_value == right_value.string_value;
}

static void first_event(data_map *dest,
        timestamp UNUSED(ls), timestamp UNUSED(le), data_map *left,
        timestamp UNUSED(rs), timestamp UNUSED(re), data_map *UNUSED(right)) {
    map_value value;
    map_get(left, 0, &value);
    map_set(dest, 0, &value);
}

void test_beaglebone_intervals(void) {
    label int_enter = 0, int_exit = 1, hand_enter = 2, hand_exit = 3,
            interrupt = 4, handler = 5, handled = 6;
    map_key event = 0;
    map_value v44, v29, check_map, expected_map;
    interval intervals[] = {
            { int_enter, 10, 10, EMPTY_MAP, false },
            { hand_enter, 20, 20, EMPTY_MAP, false },
            { int_enter, 25, 25, EMPTY_MAP, false },
            { hand_exit, 30, 30, EMPTY_MAP, false },
            { hand_enter, 35, 35, EMPTY_MAP, false },
            { int_exit, 40, 40, EMPTY_MAP, false },
            { hand_exit, 45, 45, EMPTY_MAP, false },
            { int_exit, 55, 55, EMPTY_MAP, false }
    };
    pool in, out;
    pool_iterator pit;
    interval *check;
    int i;
    phi_function equal_phi = { "EQUAL_EVENT", equal_event_string, first_event };

    setup();
    initialize_pool(&in);
    initialize_pool(&out);

    v44.type = string_type;
    v44.string_value = 0;
    v29.type = string_type;
    v29.string_value = 1;

    // add all the test intervals to the pool
    for (i = 0; i < 8; i++) {
        initialize_map(&intervals[i].map);
        // a lazy way of differentiating...
        if (intervals[i].start % 10 == 0) {
            map_set(&intervals[i].map, event, &v44);
        } else {
            map_set(&intervals[i].map, event, &v29);
        }
        add_interval(&in, &intervals[i]);
    }

    resize_specification(&spec, 7);
    add_rule_to_specification(&spec, interrupt, int_enter, BEFORE_OPERATOR, int_exit, &equal_phi);
    add_rule_to_specification(&spec, handler, hand_enter, BEFORE_OPERATOR, hand_exit, &equal_phi);
    add_rule_to_specification(&spec, handled, handler, DURING_OPERATOR, interrupt, &equal_phi);

    // actually run nfer
    run_nfer(&spec, &in, &out);

    assert_int_equals("result size is wrong", 6, out.size);

    get_pool_iterator(&out, &pit);
    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("1 result label is wrong", handler, check->name);
    assert_int_equals("1 result start is wrong", intervals[1].start, check->start);
    assert_int_equals("1 result end is wrong", intervals[3].end, check->end);
    map_get(&intervals[1].map, event, &expected_map);
    assert_int_equals("1 map value is wrong", expected_map.string_value, check_map.string_value);

    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("2 result label is wrong", interrupt, check->name);
    assert_int_equals("2 result start is wrong", intervals[0].start, check->start);
    assert_int_equals("2 result end is wrong", intervals[5].end, check->end);
    map_get(&intervals[0].map, event, &expected_map);
    assert_int_equals("2 map value is wrong", expected_map.string_value, check_map.string_value);

    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("3 result label is wrong", handled, check->name);
    assert_int_equals("3 result start is wrong", intervals[0].start, check->start);
    assert_int_equals("3 result end is wrong", intervals[5].end, check->end);
    map_get(&intervals[0].map, event, &expected_map);
    assert_int_equals("3 map value is wrong", expected_map.string_value, check_map.string_value);

    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("4 result label is wrong", handler, check->name);
    assert_int_equals("4 result start is wrong", intervals[4].start, check->start);
    assert_int_equals("4 result end is wrong", intervals[6].end, check->end);
    map_get(&intervals[4].map, event, &expected_map);
    assert_int_equals("4 map value is wrong", expected_map.string_value, check_map.string_value);

    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("5 result label is wrong", interrupt, check->name);
    assert_int_equals("5 result start is wrong", intervals[2].start, check->start);
    assert_int_equals("5 result end is wrong", intervals[7].end, check->end);
    map_get(&intervals[2].map, event, &expected_map);
    assert_int_equals("5 map value is wrong", expected_map.string_value, check_map.string_value);

    check = next_interval(&pit);
    map_get(&check->map, event, &check_map);
    assert_int_equals("6 result label is wrong", handled, check->name);
    assert_int_equals("6 result start is wrong", intervals[2].start, check->start);
    assert_int_equals("6 result end is wrong", intervals[7].end, check->end);
    map_get(&intervals[2].map, event, &expected_map);
    assert_int_equals("6 map value is wrong", expected_map.string_value, check_map.string_value);

    destroy_pool(&out);
    destroy_pool(&in);
    teardown();
}

void test_nfer_dsl(void) {
    label boot_s = 0, downlink = 1, boot_e = 2, boot = 3;
    word_id a = 10, d = 11, f = 12;
    map_key count = 2;
    map_value count_value, check_map_value;
    interval intervals[] = {
            { boot_s, 40, 40, EMPTY_MAP, false },
            { downlink, 41, 41, EMPTY_MAP, false },
            { boot_s, 42, 42, EMPTY_MAP, false },
            { boot_s, 44, 44, EMPTY_MAP, false },
            { boot_e, 46, 46, EMPTY_MAP, false },
            { downlink, 48, 48, EMPTY_MAP, false },
            { boot_e, 50, 50, EMPTY_MAP, false }
    };
    pool in, out;
    interval *check;
    int i;
    expression_input *where_clause, *begin_clause, *end_clause, *map_clause;

    setup();
    initialize_pool(&in);
    initialize_pool(&out);

    count_value.type = string_type;
    count_value.string_value = a;
    map_set(&intervals[2].map, count, &count_value);
    count_value.type = string_type;
    count_value.string_value = f;
    map_set(&intervals[0].map, count, &count_value);
    map_set(&intervals[4].map, count, &count_value);
    count_value.type = string_type;
    count_value.string_value = d;
    map_set(&intervals[3].map, count, &count_value);
    map_set(&intervals[6].map, count, &count_value);

    // add all the test intervals to the pool
    for (i = 0; i < 7; i++) {
        add_interval(&in, &intervals[i]);
        destroy_map(&intervals[i].map);
    }

    add_rule_to_specification(&spec, boot, boot_s, ALSO_OPERATOR, boot_e, NULL);
    // where lhs.end < rhs.begin & lhs.count = rhs.count
    initialize_expression_input(&where_clause, 10);
    where_clause[0].length = 10;
    where_clause[1].action = param_left_end;
    where_clause[2].action = param_right_begin;
    where_clause[3].action = action_lt;
    where_clause[4].action = param_left_field;
    where_clause[5].string_value = count;
    where_clause[6].action = param_right_field;
    where_clause[7].string_value = count;
    where_clause[8].action = action_eq;
    where_clause[9].action = action_and;
    spec.rule_list.rules[0].where_expression = where_clause;

    initialize_expression_input(&begin_clause, 2);
    begin_clause[0].length = 2;
    begin_clause[1].action = param_left_begin;
    spec.rule_list.rules[0].begin_expression = begin_clause;

    initialize_expression_input(&end_clause, 2);
    end_clause[0].length = 2;
    end_clause[1].action = param_right_end;
    spec.rule_list.rules[0].end_expression = end_clause;

    initialize_expression_input(&map_clause, 3);
    map_clause[0].length = 3;
    map_clause[1].action = param_left_field;
    map_clause[2].string_value = count;
    count_value.type = pointer_type;
    count_value.pointer_value = map_clause;
    map_set(&spec.rule_list.rules[0].map_expressions, count, &count_value);

    // actually run nfer
    run_nfer(&spec, &in, &out);

    assert_int_equals("result size is wrong", 2, out.size);
    i = 0;

    check = &out.intervals[i++].i;
    assert_int_equals("result label is wrong", boot, check->name);
    assert_int_equals("result start is wrong", intervals[0].start, check->start);
    assert_int_equals("result end is wrong", intervals[4].end, check->end);
    map_get(&check->map, count, &check_map_value);
    assert_int_equals("result map is wrong", f, check_map_value.string_value);

    check = &out.intervals[i++].i;
    assert_int_equals("result label is wrong", boot, check->name);
    assert_int_equals("result start is wrong", intervals[3].start, check->start);
    assert_int_equals("result end is wrong", intervals[6].end, check->end);
    map_get(&check->map, count, &check_map_value);
    assert_int_equals("result map is wrong", d, check_map_value.string_value);

    destroy_pool(&out);
    destroy_pool(&in);
    teardown();
}
