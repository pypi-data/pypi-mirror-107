/*
 * types.c
 *
 *  Created on: Jun 7, 2017
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


bool equals(typed_value *left, typed_value *right) {
    // if both are null pointers, then I suppose they're equal?
    if (left == NULL && right == NULL) {
        return true;
    }

    // if one is a null pointer, though, then they're definitely not equal
    if (left == NULL || right == NULL) {
        return false;
    }

    // if their types aren't equal, then they aren't equal
    if (left->type != right->type) {
        return false;
    }

    switch(left->type) {
    case null_type:
        // both are null, so they are equal
        return true;
        break;
    case boolean_type:
        // just compare the boolean values
        return left->boolean_value == right->boolean_value;
        break;
    case integer_type:
        // just compare the integer values
        return left->integer_value == right->integer_value;
        break;
    case real_type:
        // just compare the real values
        return left->real_value == right->real_value;
        break;
    case string_type:
        // just compare the string values
        return left->string_value == right->string_value;
        break;
    case pointer_type:
        // just compare the pointer values
        return left->pointer_value == right->pointer_value;
        break;
    }

    // provide a default case to make the compiler happy
    return false;
}
