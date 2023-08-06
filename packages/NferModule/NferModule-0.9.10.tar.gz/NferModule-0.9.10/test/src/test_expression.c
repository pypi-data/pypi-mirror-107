/*
 * test_eval.c
 *
 *  Created on: May 1, 2017
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

#include <stdlib.h>

#include "types.h"
#include "test.h"
#include "stack.h"
#include "map.h"
#include "pool.h"
#include "expression.h"
#include "test_expression.h"


#define MAX_ACTION_SIZE 8

static expression_input *input;
static data_stack stack;
static data_map map1, map2;

static void setup(void) {
    initialize_expression_input(&input, MAX_ACTION_SIZE);
    initialize_stack(&stack);
    initialize_map(&map1);
    initialize_map(&map2);
}
static void teardown(void) {
    destroy_expression_input(&input);
    destroy_stack(&stack);
    destroy_map(&map1);
    destroy_map(&map2);
}


void test_expression_from_input(void) {
    int position = 1;
    typed_value result;
    setup();

    input[position++].action = param_intlit;
    input[position++].integer_value = 4;
    input[position++].action = param_reallit;
    input[position++].real_value = 4.5;
    input[position++].action = action_add;
    input[0].length = position;

    evaluate_expression(input, &result, &stack,
            0, 0, NULL, 0, 0, NULL);

    assert_int_equals("stack should be empty", 0, stack.tos);
    assert_int_equals("result type wrong", real_type, result.type);
    assert_float_equals("result value wrong", 8.5, result.real_value);

    input[position++].action = param_intlit;
    input[position++].integer_value = 10;
    input[position++].action = action_lt;
    input[0].length = position;

    evaluate_expression(input, &result, &stack,
            0, 0, NULL, 0, 0, NULL);

    assert_int_equals("stack should be empty", 0, stack.tos);
    assert_int_equals("result type wrong", boolean_type, result.type);
    assert_true("result value wrong", result.boolean_value);

    teardown();
}
void test_expression_from_runtime(void) {
    int position = 1;
    typed_value result;
    map_value value;
    setup();

    value.type = integer_type;
    value.integer_value = 10;
    map_set(&map1, 0, &value);
    input[position++].action = param_left_field;
    input[position++].field_name = 0;
    value.type = integer_type;
    value.integer_value = 20;
    map_set(&map2, 1, &value);
    input[position++].action = param_right_field;
    input[position++].field_name = 1;
    input[position++].action = action_mul;
    input[0].length = position;

    evaluate_expression(input, &result, &stack,
            0, 0, &map1, 0, 0, &map2);

    assert_int_equals("stack should be empty", 0, stack.tos);
    assert_int_equals("result type wrong", integer_type, result.type);
    assert_int_equals("result value wrong", 200, result.integer_value);

    input[position++].action = param_left_end;
    input[position++].action = action_sub;
    input[position++].action = action_neg;
    input[0].length = position;

    evaluate_expression(input, &result, &stack,
            10, 20, &map1, 30, 40, &map2);

    assert_int_equals("stack should be empty", 0, stack.tos);
    assert_int_equals("result type wrong", integer_type, result.type);
    assert_int_equals("result value wrong", -180, result.integer_value);

    teardown();
}
