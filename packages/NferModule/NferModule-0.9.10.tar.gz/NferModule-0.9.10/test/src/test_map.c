/*
 * test_map.c
 *
 *  Created on: Apr 3, 2017
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


#include "test.h"
#include "test_map.h"
#include "map.h"

static data_map map;

static void setup(void) {
    initialize_map(&map);
}

static void teardown(void) {
    destroy_map(&map);
}

void test_initialize_map(void) {
    setup();

    assert_int_equals("map should be empty", 0, map.space);
    assert_null("values should be null", map.values);

    teardown();
}
void test_destroy_map(void) {
    setup();

    teardown();

    assert_int_equals("map should be empty", 0, map.space);
    assert_null("values should be null", map.values);
}
void test_map_set(void) {
    int i;
    map_value v;
    setup();

    v.type = string_type;
    v.string_value = 1;

    assert_int_equals("start should not be set", MAP_MISSING_KEY, map.start);

    map_set(&map, 2, &v);
    assert_int_equals("space should have grown", 2 + MAP_SIZE_INCREMENT, map.space);
    assert_int_equals("type should be set", v.type, map.values[2].value.type);
    assert_int_equals("value should be set", v.string_value, map.values[2].value.string_value);
    assert_int_equals("start is wrong", 2, map.start);
    assert_int_equals("next is wrong", MAP_MISSING_KEY, map.values[2].next);
    assert_int_equals("prior is wrong", MAP_MISSING_KEY, map.values[2].prior);

    for (i = 0; i < map.space; i++) {
        if (i != 2) {
            assert_int_equals("other types should be null", null_type, map.values[i].value.type);
        }
    }

    v.string_value = 2;
    map_set(&map, 1, &v);
    assert_int_equals("space should not have grown", 2 + MAP_SIZE_INCREMENT, map.space);
    assert_int_equals("type should be set", v.type, map.values[1].value.type);
    assert_int_equals("value should be set", v.string_value, map.values[1].value.string_value);
    assert_int_equals("start is wrong", 1, map.start);
    assert_int_equals("next is wrong", 2, map.values[1].next);
    assert_int_equals("prior is wrong", MAP_MISSING_KEY, map.values[1].prior);
    assert_int_equals("prior is wrong", 1, map.values[2].prior);

    v.type = real_type;
    v.real_value = 3.14;
    map_set(&map, 2, &v);
    assert_int_equals("space should not have grown", 2 + MAP_SIZE_INCREMENT, map.space);
    assert_int_equals("type should be set", v.type, map.values[2].value.type);
    assert_int_equals("value should be set", v.real_value, map.values[2].value.real_value);
    assert_int_equals("start is wrong", 1, map.start);
    assert_int_equals("next is wrong", 2, map.values[1].next);
    assert_int_equals("prior is wrong", MAP_MISSING_KEY, map.values[1].prior);
    assert_int_equals("prior is wrong", 1, map.values[2].prior);

    v.real_value = 6.28;
    map_set(&map, 2 + MAP_SIZE_INCREMENT, &v);
    assert_int_equals("space should have grown", 2 + (MAP_SIZE_INCREMENT * 2), map.space);
    assert_int_equals("type should be set", v.type, map.values[2 + MAP_SIZE_INCREMENT].value.type);
    assert_int_equals("value should be set", v.real_value, map.values[2 + MAP_SIZE_INCREMENT].value.real_value);
    assert_int_equals("start is wrong", 2 + MAP_SIZE_INCREMENT, map.start);
    assert_int_equals("next is wrong", 1, map.values[2 + MAP_SIZE_INCREMENT].next);
    assert_int_equals("prior is wrong", MAP_MISSING_KEY, map.values[2 + MAP_SIZE_INCREMENT].prior);
    assert_int_equals("prior is wrong", 2 + MAP_SIZE_INCREMENT, map.values[1].prior);

    for (i = 0; i < map.space; i++) {
        if (i != 1 && i != 2 && i != 2 + MAP_SIZE_INCREMENT) {
            assert_int_equals("other types should be null", null_type, map.values[i].value.type);
        }
    }

    teardown();
}
void test_map_get(void) {
    map_value set_value, value;
    setup();

    map_get(&map, 0, &value);
    assert_int_equals("should be missing value", null_type, value.type);
    assert_int_equals("should not have resized map", 0, map.space);
    assert_null("values should be null", map.values);

    map_get(&map, 1, &value);
    assert_int_equals("should be missing value", null_type, value.type);

    set_value.type = boolean_type;
    set_value.boolean_value = true;
    map_set(&map, 5, &set_value);
    set_value.type = integer_type;
    set_value.integer_value = 33;
    map_set(&map, 3, &set_value);

    map_get(&map, 0, &value);
    assert_int_equals("should be missing value", null_type, value.type);
    map_get(&map, 1, &value);
    assert_int_equals("should be missing value", null_type, value.type);

    map_get(&map, 5, &value);
    assert_int_equals("type should be set", boolean_type, value.type);
    assert_int_equals("key should be set", true, value.boolean_value);
    map_get(&map, 3, &value);
    assert_int_equals("type should be set", integer_type, value.type);
    assert_int_equals("key should be set", 33, value.integer_value);

    teardown();
}
void test_map_find(void) {
    map_key key;
    map_value value1, value2, value3;

    setup();

    value1.type = integer_type;
    value1.integer_value = 150;

    value2.type = string_type;
    value2.string_value = 2;

    map_set(&map, 3, &value1);
    map_set(&map, 1, &value2);

    key = map_find(&map, &value1);
    assert_int_equals("should find value", 3, key);

    key = map_find(&map, &value2);
    assert_int_equals("should find value", 1, key);

    value3.type = integer_type;
    value3.integer_value = 100;

    key = map_find(&map, &value3);
    assert_int_equals("should not find value", MAP_MISSING_KEY, key);

    teardown();
}
