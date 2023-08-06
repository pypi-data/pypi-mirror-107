/*
 * test_strings.c
 *
 *  Created on: May 15, 2018
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

#include "strings.h"
#include "test.h"

static void reset_dest(char *dest, char set, int max) {
    int i;
    // set dest to predictable values
    for (i = 0; i < max; i++) {
        dest[i] = set;
    }
}

void test_copy_string(void) {
    char dest[20];
    char *numbers = "1234567890";
    char *letters = "abcdefghijklmnopqrstuvwxyz";
    int i;

    reset_dest(dest, '\n', 20);

    // stop at the end of the src string
    copy_string(dest, numbers, 19);
    assert_str_equals("Numbers not copied", numbers, dest);
    assert_int_equals("Null not set", '\0', dest[10]);
    for (i = 11; i < 20; i++) {
        assert_int_equals("Character improperly overwritten", '\n', dest[i]);
    }

    reset_dest(dest, '\n', 20);

    // stop at the end of the src string
    copy_string(dest, letters, 10);
    assert_str_equals("Numbers not copied", "abcdefghij", dest);
    assert_int_equals("Null not set", '\0', dest[10]);
    for (i = 11; i < 20; i++) {
        assert_int_equals("Character improperly overwritten", '\n', dest[i]);
    }
}
void test_string_equals(void) {
    char *numbers = "1234567890";
    char *letters = "abcdefghijklmnopqrstuvwxyz";
    char *lesslet = "abcdefghij";

    assert_true("Numbers should be equal", string_equals(numbers, numbers, 20));
    assert_true("Beginning of numbers should be equal", string_equals(numbers, numbers, 5));
    assert_false("Numbers and letters should not be equal", string_equals(numbers, letters, 20));
    assert_false("Letters and less letters should not be equal", string_equals(letters, lesslet, 11));
    assert_true("Beginning of letters should be equal", string_equals(letters, lesslet, 10));
}
void test_string_length(void) {
    char *nully = (char *)0;
    char *empty = "";
    char *numbers = "1234567890";

    assert_int_equals("Null string should have length zero", 0, string_length(nully, 20));
    assert_int_equals("Empty string should have length zero", 0, string_length(empty, 20));
    assert_int_equals("Numbers should have length 10", 10, string_length(numbers, 20));
    assert_int_equals("Numbers should have length 10 when max is 10", 10, string_length(numbers, 10));
    assert_int_equals("Max length should be respected", 4, string_length(numbers, 4));
}
void test_string_to_u64(void) {
    char *nully = (char *)0;
    char *empty = "";
    char *numbers = "1234567890";
    char *real = "123.456";
    char *nums_and_letters = "456and789";

    assert_int_equals("Null string should be zero", 0, string_to_u64(nully, 20));
    assert_int_equals("Empty string should be zero", 0, string_to_u64(empty, 20));
    assert_int_equals("Numbers should be parsed", 1234567890, string_to_u64(numbers, 20));
    assert_int_equals("Max length should be respected", 1234, string_to_u64(numbers, 4));
    assert_int_equals("Real number should be truncated", 123, string_to_u64(real, 5));
    assert_int_equals("First string should be parsed", 456, string_to_u64(nums_and_letters, 20));
}
void test_string_to_i64(void) {
    char *nully = (char *)0;
    char *empty = "";
    char *numbers = "1234567890";
    char *sign = "-";
    char *negative = "-1234567890";
    char *real = "123.456";
    char *neg_real = "-123.456";

    assert_int_equals("Null string should be zero", 0, string_to_i64(nully, 20));
    assert_int_equals("Empty string should be zero", 0, string_to_i64(empty, 20));
    assert_int_equals("Numbers should be parsed", 1234567890, string_to_i64(numbers, 20));
    assert_int_equals("Negative sign should be zero", 0, string_to_i64(sign, 20));
    assert_int_equals("Negative numbers should be parsed", -1234567890, string_to_i64(negative, 20));
    assert_int_equals("Max length should be respected", -1234, string_to_i64(negative, 5));
    assert_int_equals("Real number should be truncated", 123, string_to_i64(real, 5));
    assert_int_equals("Negative real number should be truncated", -123, string_to_i64(neg_real, 6));
}
void test_string_to_double(void) {
    char *nully = (char *)0;
    char *empty = "";
    char *numbers = "1234567890";
    char *sign = "-";
    char *negative = "-1234567890";
    char *real = "123.456";
    char *neg_real = "-123.456";
    char *dot_start = ".789";

    assert_float_equals("Null string should be zero", 0.0, string_to_double(nully, 20));
    assert_float_equals("Empty string should be zero", 0.0, string_to_double(empty, 20));
    assert_float_equals("Numbers should be parsed", 1234567890, string_to_double(numbers, 20));
    assert_float_equals("Negative sign should be zero", 0, string_to_double(sign, 20));
    assert_float_equals("Negative numbers should be parsed", -1234567890, string_to_double(negative, 20));
    assert_float_equals("Max length should be respected", -1234, string_to_double(negative, 5));
    assert_float_equals("Real number should be parsed", 123.456, string_to_double(real, 20));
    assert_float_equals("Negative real number should be truncated", -123.456, string_to_double(neg_real, 20));
    assert_float_equals("Max length should be respected", -123.4, string_to_double(neg_real, 6));
    assert_float_equals("Floats that start with dot should work", 0.789, string_to_double(dot_start, 5));
}
