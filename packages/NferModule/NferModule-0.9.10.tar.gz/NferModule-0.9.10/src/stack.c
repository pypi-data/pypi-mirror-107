/*
 * stack.c
 *
 *  Created on: Apr 29, 2017
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

#include "stack.h"


void initialize_stack(data_stack *stack) {
    stack->values = NULL;
#ifndef NO_DYNAMIC_MEMORY
    stack->values = malloc(sizeof(stack_value) * INITIAL_STACK_SPACE);
    if (stack->values != NULL) {
        stack->space = INITIAL_STACK_SPACE;
    }
#endif
    stack->tos = 0;
}
void destroy_stack(data_stack *stack) {
    stack->space = 0;
    stack->tos = 0;
#ifndef NO_DYNAMIC_MEMORY
    if (stack->values != NULL) {
        free(stack->values);
        stack->values = NULL;
    }
#endif
}
void push(data_stack *stack, stack_value *value) {
#ifndef NO_DYNAMIC_MEMORY
    if (stack->tos >= stack->space) {
        stack->values = realloc(stack->values, sizeof(stack_value) * stack->space * 2);

        if (stack->values != NULL) {
            stack->space = stack->space * 2;
        } else {
            stack->space = 0;
            stack->tos = 0;
            // bail out, since we failed to realloc
            return;
        }
    }
#endif

    if (stack->tos < stack->space) {
        stack->values[stack->tos].type = value->type;
        switch(value->type) {
        case null_type:
            stack->values[stack->tos].boolean_value = false;
            break;
        case boolean_type:
            stack->values[stack->tos].boolean_value = value->boolean_value;
            break;
        case integer_type:
            stack->values[stack->tos].integer_value = value->integer_value;
            break;
        case real_type:
            stack->values[stack->tos].real_value = value->real_value;
            break;
        case string_type:
            stack->values[stack->tos].string_value = value->string_value;
            break;
        case pointer_type:
            stack->values[stack->tos].pointer_value = value->pointer_value;
            break;
        }
        stack->tos++;
    }
}
void pop(data_stack *stack, stack_value *value) {
    if (stack->tos > 0) {
        stack->tos--;
        value->type = stack->values[stack->tos].type;
        switch(value->type) {
        case null_type:
            value->boolean_value = false;
            break;
        case boolean_type:
            value->boolean_value = stack->values[stack->tos].boolean_value;
            break;
        case integer_type:
            value->integer_value = stack->values[stack->tos].integer_value;
            break;
        case real_type:
            value->real_value = stack->values[stack->tos].real_value;
            break;
        case string_type:
            value->string_value = stack->values[stack->tos].string_value;
            break;
        case pointer_type:
            value->pointer_value = stack->values[stack->tos].pointer_value;
            break;
        }
    } else {
        value->type = null_type;
        value->boolean_value = false;
    }
}
