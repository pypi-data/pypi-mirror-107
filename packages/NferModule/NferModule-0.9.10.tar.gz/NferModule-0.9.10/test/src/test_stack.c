/*
 * test_stack.c
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


#include "types.h"
#include "stack.h"
#include "test_stack.h"
#include "test.h"

static data_stack stack;

static void setup(void) {
    initialize_stack(&stack);
}
static void teardown(void) {
    destroy_stack(&stack);
}

void test_initialize_stack(void) {
    setup();

    assert_int_equals("stack space should be set", INITIAL_STACK_SPACE, stack.space);
    assert_int_equals("tos should be 0", 0, stack.tos);
    assert_not_null("stack values should not be null", stack.values);

    teardown();
}
void test_destroy_stack(void) {
    setup();
    teardown();

    assert_int_equals("stack space should be 0", 0, stack.space);
    assert_int_equals("tos should be 0", 0, stack.tos);
    assert_null("stack values should be null", stack.values);
}
void test_push(void) {
    stack_value value1, value2, result;
    int i;
    setup();

    value1.type = string_type;
    value1.string_value = 3;

    for (i = 0; i < INITIAL_STACK_SPACE; i++) {
        push(&stack, &value1);
    }

    value2.type = boolean_type;
    value2.boolean_value = true;
    push(&stack, &value2);

    assert_int_equals("stack should have grown", INITIAL_STACK_SPACE * 2, stack.space);
    pop(&stack, &result);
    assert_int_equals("popped type wrong", value2.type, result.type);
    assert_int_equals("popped value wrong", value2.real_value, result.real_value);

    assert_int_equals("stack should not have shrunk", INITIAL_STACK_SPACE * 2, stack.space);
    pop(&stack, &result);
    assert_int_equals("popped type wrong", value1.type, result.type);
    assert_int_equals("popped value wrong", value1.real_value, result.real_value);

    teardown();
}
void test_pop(void) {
    stack_value value1, value2, result;
    setup();

    value1.type = real_type;
    value1.real_value = 5.4;

    value2.type = integer_type;
    value2.integer_value = 9;

    push(&stack, &value1);
    push(&stack, &value2);

    assert_int_equals("stack tos wrong", 2, stack.tos);

    pop(&stack, &result);
    assert_int_equals("popped type wrong", value2.type, result.type);
    assert_int_equals("popped value wrong", value2.real_value, result.real_value);
    assert_int_equals("stack tos wrong", 1, stack.tos);

    pop(&stack, &result);
    assert_int_equals("popped type wrong", value1.type, result.type);
    assert_int_equals("popped value wrong", value1.real_value, result.real_value);
    assert_int_equals("stack tos wrong", 0, stack.tos);

    pop(&stack, &result);
    assert_int_equals("popped type wrong", null_type, result.type);
    assert_int_equals("stack tos wrong", 0, stack.tos);

    teardown();
}
