/*
 * test_memory.c
 *
 *  Created on: May 14, 2018
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

#include "memory.h"
#include "test.h"

typedef struct _test_type {
    long int one;
    int two;
    short int three;
    char four;
    char five;
} test_type;

void test_set_memory(void) {
    char small_data[3];
    long int big_data[20];
    long int equal_data;
    test_type weird_data;
    int i;

    // clear everything first
    for (i = 0; i < 3; i++) {
        small_data[i] = 0;
    }

    for (i = 0; i < 20; i++) {
        big_data[i] = 0;
    }

    equal_data = 0;

    weird_data.one = 0;
    weird_data.two = 0;
    weird_data.three = 0;
    weird_data.four = 0;
    weird_data.five = 0;

    set_memory(small_data, 3 * sizeof(char));
    for (i = 0; i < 3; i++) {
        assert_true("Small data not properly set", (char)0xff == small_data[i]);
    }
    set_memory(big_data, 20 * sizeof(long int));
    for (i = 0; i < 20; i++) {
        assert_true("Big data not properly set", (long int)0xffffffffffffffffUL == big_data[i]);
    }
    set_memory(&equal_data, sizeof(long int));
    assert_true("Equal data not properly set", (long int)0xffffffffffffffffUL == equal_data);
    set_memory(&weird_data, sizeof(long int) + sizeof(int) + sizeof(short int) + sizeof(char));
    assert_true("Weird data one not properly set", (long int)0xffffffffffffffffUL == weird_data.one);
    assert_true("Weird data two not properly set", (int)0xffffffff == weird_data.two);
    assert_true("Weird data three not properly set", (short int)0xffff == weird_data.three);
    assert_true("Weird data four not properly set", (char)0xff == weird_data.four);
    assert_true("Weird data five should not be set", (char)0x00 == weird_data.five);
}

void test_clear_memory(void) {
    char small_data[3];
    long int big_data[20];
    long int equal_data;
    test_type weird_data;
    int i;

    // set everything first
    for (i = 0; i < 3; i++) {
        small_data[i] = 0xff;
    }

    for (i = 0; i < 20; i++) {
        big_data[i] = 0xffffffffffffffffUL;
    }

    equal_data = 0xffffffffffffffffUL;

    weird_data.one = 0xffffffffffffffffUL;
    weird_data.two = 0xffffffff;
    weird_data.three = 0xffff;
    weird_data.four = 0xff;
    weird_data.five = 0xff;

    clear_memory(small_data, 3 * sizeof(char));
    for (i = 0; i < 3; i++) {
        assert_true("Small data not properly cleared", (char)0x00 == small_data[i]);
    }
    clear_memory(big_data, 20 * sizeof(long int));
    for (i = 0; i < 20; i++) {
        assert_true("Big data not properly cleared", (long int)0x00 == big_data[i]);
    }
    clear_memory(&equal_data, sizeof(long int));
    assert_true("Equal data not properly cleared", (long int)0x00 == equal_data);
    clear_memory(&weird_data, sizeof(long int) + sizeof(int) + sizeof(short int) + sizeof(char));
    assert_true("Weird data one not properly cleared", (long int)0x00 == weird_data.one);
    assert_true("Weird data two not properly cleared", (int)0x00 == weird_data.two);
    assert_true("Weird data three not properly cleared", (short int)0x00 == weird_data.three);
    assert_true("Weird data four not properly cleared", (char)0x00 == weird_data.four);
    assert_true("Weird data five should not be cleared", (char)0xff == weird_data.five);
}
void test_copy_memory(void) {
    char small_data_to[3];
    long int big_data_to[20];
    long int equal_data_to;
    test_type weird_data_to;
    int i;
    unsigned char from[20][8];

    // clear everything first
    for (i = 0; i < 3; i++) {
        small_data_to[i] = 0;
    }

    for (i = 0; i < 20; i++) {
        big_data_to[i] = 0;
    }

    equal_data_to = 0;

    weird_data_to.one = 0;
    weird_data_to.two = 0;
    weird_data_to.three = 0;
    weird_data_to.four = 0;
    weird_data_to.five = 0;

    for (i = 0; i < 20; i++) {
        from[i][0] = 0x12; //0x1234567890ABCDEFUL, but specify endianness
        from[i][1] = 0x34;
        from[i][2] = 0x56;
        from[i][3] = 0x78;
        from[i][4] = 0x90;
        from[i][5] = 0xab;
        from[i][6] = 0xcd;
        from[i][7] = 0xef;
    }

    copy_memory(small_data_to, from, 3 * sizeof(char));
    assert_true("Small data 0 not properly set", (char)0x12 == small_data_to[0]);
    assert_true("Small data 1 not properly set", (char)0x34 == small_data_to[1]);
    assert_true("Small data 2 not properly set", (char)0x56 == small_data_to[2]);


    copy_memory(big_data_to, from, 20 * sizeof(long int));
    for (i = 0; i < 20; i++) {
        assert_true("Big data 0 not properly set", (char)0x12 == ((char *)&big_data_to[i])[0]);
        assert_true("Big data 1 not properly set", (char)0x34 == ((char *)&big_data_to[i])[1]);
        assert_true("Big data 2 not properly set", (char)0x56 == ((char *)&big_data_to[i])[2]);
        assert_true("Big data 3 not properly set", (char)0x78 == ((char *)&big_data_to[i])[3]);
        assert_true("Big data 4 not properly set", (char)0x90 == ((char *)&big_data_to[i])[4]);
        assert_true("Big data 5 not properly set", (char)0xab == ((char *)&big_data_to[i])[5]);
        assert_true("Big data 6 not properly set", (char)0xcd == ((char *)&big_data_to[i])[6]);
        assert_true("Big data 7 not properly set", (char)0xef == ((char *)&big_data_to[i])[7]);
    }

    copy_memory(&equal_data_to, from, sizeof(long int));
    assert_true("Equal data 0 not properly set", (char)0x12 == ((char *)&equal_data_to)[0]);
    assert_true("Equal data 1 not properly set", (char)0x34 == ((char *)&equal_data_to)[1]);
    assert_true("Equal data 2 not properly set", (char)0x56 == ((char *)&equal_data_to)[2]);
    assert_true("Equal data 3 not properly set", (char)0x78 == ((char *)&equal_data_to)[3]);
    assert_true("Equal data 4 not properly set", (char)0x90 == ((char *)&equal_data_to)[4]);
    assert_true("Equal data 5 not properly set", (char)0xab == ((char *)&equal_data_to)[5]);
    assert_true("Equal data 6 not properly set", (char)0xcd == ((char *)&equal_data_to)[6]);
    assert_true("Equal data 7 not properly set", (char)0xef == ((char *)&equal_data_to)[7]);

    copy_memory(&weird_data_to, from, sizeof(long int) + sizeof(int) + sizeof(short int) + sizeof(char));
    assert_true("Weird data one 0 not properly set", (char)0x12 == ((char *)&weird_data_to.one)[0]);
    assert_true("Weird data one 1 not properly set", (char)0x34 == ((char *)&weird_data_to.one)[1]);
    assert_true("Weird data one 2 not properly set", (char)0x56 == ((char *)&weird_data_to.one)[2]);
    assert_true("Weird data one 3 not properly set", (char)0x78 == ((char *)&weird_data_to.one)[3]);
    assert_true("Weird data one 4 not properly set", (char)0x90 == ((char *)&weird_data_to.one)[4]);
    assert_true("Weird data one 5 not properly set", (char)0xab == ((char *)&weird_data_to.one)[5]);
    assert_true("Weird data one 6 not properly set", (char)0xcd == ((char *)&weird_data_to.one)[6]);
    assert_true("Weird data one 7 not properly set", (char)0xef == ((char *)&weird_data_to.one)[7]);

    assert_true("Weird data two 0 not properly set", (char)0x12 == ((char *)&weird_data_to.two)[0]);
    assert_true("Weird data two 1 not properly set", (char)0x34 == ((char *)&weird_data_to.two)[1]);
    assert_true("Weird data two 2 not properly set", (char)0x56 == ((char *)&weird_data_to.two)[2]);
    assert_true("Weird data two 3 not properly set", (char)0x78 == ((char *)&weird_data_to.two)[3]);

    assert_true("Weird data three 4 not properly set", (char)0x90 == ((char *)&weird_data_to.three)[0]);
    assert_true("Weird data three 5 not properly set", (char)0xab == ((char *)&weird_data_to.three)[1]);

    assert_true("Weird data four not properly set", (char)0xcd == weird_data_to.four);
    assert_true("Weird data five should not be set", (char)0x00 == weird_data_to.five);
}

