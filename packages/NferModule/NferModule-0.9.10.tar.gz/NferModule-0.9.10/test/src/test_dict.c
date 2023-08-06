/*
 * test_dictionary.c
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

#include "test_dict.h"
#include "test.h"
#include "dict.h"

static dictionary dict;
static char *words[] = { "foo", "bar", "foo", "BAR", "0123456789ABCDEF0123456789ABCDEF",
        "foo5", "foo6", "foo7", "foo8", "foo9" };

static void setup(void) {
    initialize_dictionary(&dict);
}

static void teardown(void) {
    destroy_dictionary(&dict);
}

void test_initialize_dictionary(void) {
    unsigned int i;
    setup();

    assert_int_equals("size wrong", 0, dict.size);
    assert_int_equals("space wrong", INITIAL_DICTIONARY_SIZE, dict.space);
    assert_not_null("words not initialized", dict.words);
    for (i = 0; i < dict.space * sizeof(word); i++) {
        assert_int_equals("words not cleared", 0, *((char *) dict.words + i));
    }
    assert_not_null("hash not initialized", dict.hash);
    for (i = 0; i < dict.space * sizeof(word_id) * 2; i++) {
        assert_int_equals("hash not set", (char)-1, *((char *) dict.hash + i));
    }

    teardown();
}

void test_destroy_dictionary(void) {
    setup();
    teardown();
    assert_int_equals("size wrong", 0, dict.size);
    assert_int_equals("space wrong", 0, dict.space);
    assert_null("words not null", dict.words);
    assert_null("hash not null", dict.hash);
}
void test_add_word(void) {
    word_id i;
    unsigned int j;
    char toolong[MAX_WORD_LENGTH + 2];
    char truncated[MAX_WORD_LENGTH + 1];
    setup();

    // setup the toolong word
    for (j = 0; j < MAX_WORD_LENGTH + 1; j++) {
        // stick a printable ascii char in there
        toolong[j] = (j % 74) + 48;
        truncated[j] = (j % 74) + 48;
    }
    toolong[MAX_WORD_LENGTH + 1] = 0;
    truncated[MAX_WORD_LENGTH] = 0;

    // test basic adding
    i = add_word(&dict, words[0]); // add foo
    assert_int_equals("foo index wrong", 0, i);
    assert_int_equals("foo size wrong", 1, dict.size);
    i = add_word(&dict, words[1]); // add bar
    assert_int_equals("bar index wrong", 1, i);
    assert_int_equals("bar size wrong", 2, dict.size);

    // add a duplicate
    i = add_word(&dict, words[2]); // add foo from a different address
    assert_int_equals("2nd foo index wrong", 0, i);
    assert_int_equals("2nd foo size wrong", 2, dict.size);

    // add a different case word
    i = add_word(&dict, words[3]); // add BAR
    assert_int_equals("BAR index wrong", 2, i);
    assert_int_equals("BAR size wrong", 3, dict.size);

    // add a word over the max length
    i = add_word(&dict, toolong); // add too long word
    assert_int_equals("[too long] index wrong", 3, i);
    assert_str_equals("[too long] word not truncated", truncated, dict.words[i].string);
    assert_int_equals("[too long] size wrong", 4, dict.size);

    // add it again
    i = add_word(&dict, toolong); // add too long word
    assert_int_equals("2nd [too long] index wrong", 3, i);
    assert_int_equals("2nd [too long] size wrong", 4, dict.size);

    // now add more until max out space
    for (j = 5; j < 9; j++) {
        add_word(&dict, words[j]);
    }
    assert_int_equals("size wrong before resize", 8, dict.size);
    assert_int_equals("space wrong before resize", INITIAL_DICTIONARY_SIZE, dict.space);

    // check a couple of words to make sure they're still there
    i = add_word(&dict, words[3]); // add BAR
    assert_int_equals("BAR index wrong", 2, i);
    i = add_word(&dict, words[5]); // add foo5
    assert_int_equals("foo5 index wrong", 4, i);

    // now push it over the max so it has to resize
    i = add_word(&dict, words[9]);
    assert_int_equals("foo9 index wrong", 8, i);
    assert_int_equals("size wrong after resize", 9, dict.size);
    assert_int_equals("space wrong after resize", INITIAL_DICTIONARY_SIZE * 2, dict.space);
    assert_not_null("words null after resize", dict.words);
    for (j = INITIAL_DICTIONARY_SIZE * sizeof(word) + sizeof(word); j < dict.space * sizeof(word); j++) {
        assert_int_equals("words not cleared", 0, *((char *) dict.words + j));
    }
    assert_not_null("hash null after resize", dict.hash);

    // check a couple of words to make sure they're still there
    i = add_word(&dict, words[3]); // add BAR
    assert_int_equals("BAR index wrong", 2, i);
    i = add_word(&dict, words[5]); // add foo5
    assert_int_equals("foo5 index wrong", 4, i);
    i = add_word(&dict, words[9]); // add foo9
    assert_int_equals("foo9 index wrong", 8, i);

    teardown();

    assert_null("words not null", dict.words);
    i = add_word(&dict, words[0]); // should fail
    assert_int_equals("add should have failed", WORD_NOT_FOUND, i);
}
void test_get_word(void) {
    int i;
    setup();

    for (i = 0; i < 10; i++) {
        add_word(&dict, words[i]);
    }
    for (i = 0; i < 10; i++) {
        if (i < 2) {
            assert_str_equals("wrong word", words[i], get_word(&dict, i));
        } else if (i == 2) {
            assert_str_equals("wrong word", words[i], get_word(&dict, 0));
        } else {
            assert_str_equals("wrong word", words[i], get_word(&dict, i - 1));
        }
    }
    // finally try something that isn't present
    assert_null("10 should be null", get_word(&dict, 10));
    assert_null("-1 should be null", get_word(&dict, WORD_NOT_FOUND));

    teardown();
}

