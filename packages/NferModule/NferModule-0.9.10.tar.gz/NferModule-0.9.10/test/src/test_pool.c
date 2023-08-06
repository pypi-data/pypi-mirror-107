/*
 * test_pool.c
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

#include "test_pool.h"
#include "test.h"
#include "dict.h"
#include "pool.h"
#include "map.h"
#include "log.h"

static pool p;

static void setup(void) {
    initialize_pool(&p);
    // avoid warn messages
    set_log_level(LOG_LEVEL_ERROR);
}

static void teardown(void) {
    destroy_pool(&p);
}

void test_initialize_pool(void) {
    unsigned int i;
    setup();

    assert_int_equals("size wrong", 0, p.size);
    assert_int_equals("space wrong", INITIAL_POOL_SIZE, p.space);
    assert_not_null("intervals not initialized", p.intervals);
    for (i = 0; i < p.space * sizeof(interval_node); i++) {
        assert_int_equals("intervals not cleared", 0, *((char *) p.intervals + i));
    }
    assert_int_equals("start wrong", END_OF_POOL, p.start);
    assert_int_equals("end wrong", END_OF_POOL, p.end);

    teardown();
}
void test_destroy_pool(void) {
    interval add;
    setup();

    // basic add
    add.name = 4444;
    add.start = 4444;
    add.end = 4444;
    add.map = EMPTY_MAP;

    add_interval(&p, &add);

    teardown();

    assert_int_equals("size wrong", 0, p.size);
    assert_int_equals("space wrong", 0, p.space);
    assert_null("intervals not null", p.intervals);
    assert_int_equals("start wrong", END_OF_POOL, p.start);
    assert_int_equals("end wrong", END_OF_POOL, p.end);
}

void test_add_interval(void) {
    unsigned int i;
    interval add, *check;
    setup();

    // just initialize an empty map
    add.map = EMPTY_MAP;

    // basic add
    add.name = 4444;
    add.start = 4444;
    add.end = 4444;

    add_interval(&p, &add);
    check = &p.intervals[p.size - 1].i;
    assert_int_equals("size wrong", 1, p.size);
    assert_int_equals("name wrong", 4444, check->name);
    assert_int_equals("start wrong", 4444, check->start);
    assert_int_equals("end wrong", 4444, check->end);

    // add up to the end of the initial size
    for (i = 1; i < INITIAL_POOL_SIZE; i++) {
        add.name = i;
        add.start = i * 10;
        add.end = i * 100;
        add_interval(&p, &add);

        check = &p.intervals[p.size - 1].i;
        assert_int_equals("size wrong", i + 1, p.size);
        assert_int_equals("name wrong", i, check->name);
        assert_int_equals("start wrong", i * 10, check->start);
        assert_int_equals("end wrong", i * 100, check->end);
    }
    assert_int_equals("space wrong", INITIAL_POOL_SIZE, p.space);

    // make it resize
    add.name = 8888;
    add.start = 8888;
    add.end = 8888;
    add_interval(&p, &add);
    check = &p.intervals[p.size - 1].i;
    assert_int_equals("size wrong", INITIAL_POOL_SIZE + 1, p.size);
    assert_int_equals("name wrong", 8888, check->name);
    assert_int_equals("start wrong", 8888, check->start);
    assert_int_equals("end wrong", 8888, check->end);
    // check that the early records still exist but other space is clear
    check = &p.intervals[0].i;
    assert_int_equals("name wrong", 4444, check->name);
    assert_int_equals("start wrong", 4444, check->start);
    assert_int_equals("end wrong", 4444, check->end);
    for (i = 1; i < INITIAL_POOL_SIZE; i++) {
        check = &p.intervals[i].i;
        assert_int_equals("name wrong", i, check->name);
        assert_int_equals("start wrong", i * 10, check->start);
        assert_int_equals("end wrong", i * 100, check->end);
    }
    // check that the rest is cleared
    for (i = INITIAL_POOL_SIZE * sizeof(interval_node) + sizeof(interval_node); i < p.space * sizeof(interval); i++) {
        //printf("intervals(0x%x) @ 0x%x\n", (int)p.intervals, (int)((char *)p.intervals + i));
        assert_int_equals("intervals not cleared", 0, *((char *) p.intervals + i));
    }

    teardown();

    assert_null("intervals not null", p.intervals);
    add_interval(&p, &add); // should fail, but not crash
    // nothing to check here, other than that it didn't segv
}

void test_copy_pool(void) {
    interval add, *check;
    pool dest;
    int i;
    setup();
    initialize_pool(&dest);

    // just initialize an empty map
    add.map = EMPTY_MAP;

    // add some intervals to p
    for (i = 1; i < 4; i++) {
        add.name = i;
        add.start = i * 10;
        add.end = i * 100;
        add.hidden = i % 2;
        add_interval(&p, &add);
    }

    // add an interval to dest
    add.name = 0xdeadbeef;
    add.start = 0xadadb00b;
    add.end = 0xbeeff00d;
    add.hidden = false;
    add_interval(&dest, &add);

    // append p to dest
    copy_pool(&dest, &p, COPY_POOL_APPEND, COPY_POOL_INCLUDE_HIDDEN);
    assert_int_equals("1 size wrong", 3, p.size);
    assert_int_equals("1 size wrong", 4, dest.size);

    check = &dest.intervals[0].i;
    assert_int_equals("1 name wrong", (label)0xdeadbeef, check->name);
    assert_int_equals("1 start wrong", 0xadadb00b, check->start);
    assert_int_equals("1 end wrong", 0xbeeff00d, check->end);
    assert_false("1 hidden wrong", check->hidden);

    for (i = 1; i < 4; i++) {
        check = &dest.intervals[i].i;
        assert_int_equals("2 name wrong", i, check->name);
        assert_int_equals("2 start wrong", i * 10, check->start);
        assert_int_equals("2 end wrong", i * 100, check->end);
        assert_int_equals("2 hidden wrong", i % 2, check->hidden);
    }

    // copy back and overwrite p
    copy_pool(&p, &dest, COPY_POOL_OVERWRITE, COPY_POOL_INCLUDE_HIDDEN);
    assert_int_equals("3 size wrong", 4, p.size);
    assert_int_equals("3 size wrong", 4, dest.size);

    check = &p.intervals[0].i;
    assert_int_equals("3 name wrong", (label)0xdeadbeef, check->name);
    assert_int_equals("3 start wrong", 0xadadb00b, check->start);
    assert_int_equals("3 end wrong", 0xbeeff00d, check->end);
    assert_false("3 hidden wrong", check->hidden);

    for (i = 1; i < 4; i++) {
        check = &p.intervals[i].i;
        assert_int_equals("4 name wrong", i, check->name);
        assert_int_equals("4 start wrong", i * 10, check->start);
        assert_int_equals("4 end wrong", i * 100, check->end);
        assert_int_equals("4 hidden wrong", i % 2, check->hidden);
    }

    // copy back and overwrite dest, but without hidden intervals
    copy_pool(&dest, &p, COPY_POOL_OVERWRITE, COPY_POOL_EXCLUDE_HIDDEN);
    assert_int_equals("5 size wrong", 4, p.size);
    assert_int_equals("5 size wrong", 2, dest.size);

    check = &dest.intervals[0].i;
    assert_int_equals("5 name wrong", (label)0xdeadbeef, check->name);
    assert_int_equals("5 start wrong", 0xadadb00b, check->start);
    assert_int_equals("5 end wrong", 0xbeeff00d, check->end);
    assert_false("5 hidden wrong", check->hidden);

    check = &dest.intervals[1].i;
    assert_int_equals("6 name wrong", 2, check->name);
    assert_int_equals("6 start wrong", 2 * 10, check->start);
    assert_int_equals("6 end wrong", 2 * 100, check->end);
    assert_false("6 hidden wrong", check->hidden);

    destroy_pool(&dest);
    teardown();
}

//static void check_linked_list(void) {
//    pool_index i;
//    interval_node *node;
//
//    if (p.size > 0) {
//        assert_int_equals("pool start wrong", 0, p.start);
//        assert_int_equals("pool end wrong", p.size - 1, p.end);
//    }
//
//    for (i = 0; i < p.size; i++) {
//        node = &p.intervals[i];
//        assert_int_equals("interval prior wrong", (pool_index)(i - 1), node->prior);
//        if (i == p.size - 1) {
//            assert_int_equals("interval next wrong", END_OF_POOL, node->next);
//        } else {
//            assert_int_equals("interval next wrong", (pool_index)(i + 1), node->next);
//        }
//    }
//}

void test_sort_pool(void) {
    interval add, *check;
    int i;
    pool_iterator pit;
    setup();

    // just initialize an empty map
    add.map = EMPTY_MAP;

    // just sort 2 first
    add.name = 1;
    add.start = 10;
    add.end = 10;
    add_interval(&p, &add);

    add.name = 2;
    add.start = 5;
    add.end = 5;
    add_interval(&p, &add);

    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 2, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 0 wrong", 5, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 0 wrong", 10, check->end);

    // reset
    destroy_pool(&p);
    initialize_pool(&p);

    // sort 3
    add.name = 1;
    add.start = 10;
    add.end = 10;
    add_interval(&p, &add);

    add.name = 2;
    add.start = 5;
    add.end = 5;
    add_interval(&p, &add);

    add.name = 3;
    add.start = 15;
    add.end = 15;
    add_interval(&p, &add);

    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 3, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 1 wrong", 5, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 1 wrong", 10, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 1 wrong", 15, check->end);

    // reset
    destroy_pool(&p);
    initialize_pool(&p);

    // add reverse order
    for (i = 4; i > 0; i--) {
        add.name = i;
        add.start = i * 10;
        add.end = i * 10 + 5; // 45, 35, 25, 15
        add_interval(&p, &add);
    }
    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 4, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 2 wrong", 15, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 2 wrong", 25, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 2 wrong", 35, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 2 wrong", 45, check->end);

    // reset
    destroy_pool(&p);
    initialize_pool(&p);

    // add an interval to p before the generic ones
    add.name = 5;
    add.start = 1;
    add.end = 18;
    add_interval(&p, &add);

    // add some intervals to p
    for (i = 1; i < 4; i++) {
        add.name = i;
        add.start = i * 10; // 10, 20, 30
        add.end = i * 10 + 5; // 15, 25, 35
        add_interval(&p, &add);
    }

    // add an interval
    add.name = 27;
    add.start = 5; // start time is early
    add.end = 27;
    add_interval(&p, &add);
    // add an interval
    add.name = 40;
    add.start = 25;
    add.end = 40;
    add_interval(&p, &add);

    // sort
    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 6, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 15, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 18, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 25, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 27, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 35, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 3 wrong", 40, check->end);

    // reset
    destroy_pool(&p);
    initialize_pool(&p);

    add.name = 1;
    add.start = 2;
    add.end = 2;
    add_interval(&p, &add);

    add.name = 2;
    add.start = 2;
    add.end = 3;
    add_interval(&p, &add);

    add.name = 3;
    add.start = 2;
    add.end = 8;
    add_interval(&p, &add);

    add.name = 4;
    add.start = 2;
    add.end = 2;
    add_interval(&p, &add);

    add.name = 5;
    add.start = 2;
    add.end = 4;
    add_interval(&p, &add);

    add.name = 6;
    add.start = 2;
    add.end = 7;
    add_interval(&p, &add);

    // sort
    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 6, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 4 wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 4 wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 4 4wrong", 3, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 4 wrong", 4, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 4 wrong", 7, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 4 wrong", 8, check->end);

    // reset
    destroy_pool(&p);
    initialize_pool(&p);

    add.name = 1;
    add.start = 2;
    add.end = 2;
    add_interval(&p, &add);

    add.name = 2;
    add.start = 2;
    add.end = 3;
    add_interval(&p, &add);

    add.name = 3;
    add.start = 2;
    add.end = 7;
    add_interval(&p, &add);

    add.name = 4;
    add.start = 2;
    add.end = 1;
    add_interval(&p, &add);

    add.name = 5;
    add.start = 2;
    add.end = 2;
    add_interval(&p, &add);

    add.name = 6;
    add.start = 2;
    add.end = 8;
    add_interval(&p, &add);

    // sort
    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 6, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 5 wrong", 1, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 5 wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 5 5wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 5 wrong", 3, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 5 wrong", 7, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 5 wrong", 8, check->end);

    // now delete some elements, sort again and check
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    remove_from_pool(&pit);
    next_interval(&pit);
    next_interval(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    sort_pool(&p);
    get_pool_iterator(&p, &pit);

    assert_int_equals("length of p wrong", 4, p.size);

    check = next_interval(&pit);
    assert_int_equals("end 6 wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 6 5wrong", 2, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 6 wrong", 7, check->end);

    check = next_interval(&pit);
    assert_int_equals("end 6 wrong", 8, check->end);

    // also check that the intervals are packed
    assert_false("interval 0 not packed", p.intervals[0].next == END_OF_POOL);
    assert_false("interval 1 not packed", p.intervals[1].next == END_OF_POOL);
    assert_false("interval 1 not packed", p.intervals[1].prior == END_OF_POOL);
    assert_false("interval 2 not packed", p.intervals[2].next == END_OF_POOL);
    assert_false("interval 2 not packed", p.intervals[2].prior == END_OF_POOL);
    assert_false("interval 3 not packed", p.intervals[3].prior == END_OF_POOL);

    assert_int_equals("interval 4 not empty", END_OF_POOL, p.intervals[4].next);
    assert_int_equals("interval 4 not empty", END_OF_POOL, p.intervals[4].prior);
    assert_int_equals("interval 5 not empty", END_OF_POOL, p.intervals[5].next);
    assert_int_equals("interval 5 not empty", END_OF_POOL, p.intervals[5].prior);

    teardown();
}

void test_large_ts_sort(void) {
    label acquisition = 5, processing1 = 6, processing2wc = 7, processing2to5 = 8, processing2woc = 9, communication =
                10, sleep = 11, processing = 12, handling = 13, finalization = 14, ssps = 15;
    interval intervals[] = {

                { ssps, 36433289167UL, 77865924917UL, EMPTY_MAP, false },
                { sleep, 70795198750UL, 77865924917UL, EMPTY_MAP, false },
                { finalization, 70795198750UL, 77865924917UL, EMPTY_MAP, false },
                { processing, 3570703667UL, 26884595250UL, EMPTY_MAP, false },
                { sleep, 29364814584UL, 36433289167UL, EMPTY_MAP, false },
                { finalization, 26884595250UL, 36433289167UL, EMPTY_MAP, false },
                { handling, 36433289167UL, 70795198750UL, EMPTY_MAP, false },
                { processing, 45096812209UL, 70795198750UL, EMPTY_MAP, false },
                { processing2to5, 45406664209UL, 70795198750UL, EMPTY_MAP, false },
                { communication, 45406664209UL, 70795198750UL, EMPTY_MAP, false },
                { acquisition, 36433289167UL, 45096812209UL, EMPTY_MAP, false },
                { processing1, 45096812209UL, 45406664209UL, EMPTY_MAP, false },
                { processing2woc, 26884595250UL, 29364814584UL, EMPTY_MAP, false },
                { processing2to5, 3871719292UL, 29364814584UL, EMPTY_MAP, false },
                { processing1, 3570703667UL, 3871719292UL, EMPTY_MAP, false },
                { processing2wc, 3871719292UL, 26884595250UL, EMPTY_MAP, false }
    };
    int i;
    int intervals_length = sizeof(intervals) / sizeof(intervals[0]);
    pool_iterator pit;
    interval *check;
    timestamp last_end = 0, last_start = 0;
    label last_name = 0;
    bool first = true;

    setup();

    // add the test intervals to the pool
    for (i = 0; i < intervals_length; i++) {
        add_interval(&p, &intervals[i]);
    }

    sort_pool(&p);

    get_pool_iterator(&p, &pit);
    while(has_next_interval(&pit)) {
        check = next_interval(&pit);
        //log_interval(check);

        // the first one
        if (first) {
            first = false;
        } else {
            if (check->end == last_end) {
                if (check->start == last_start) {
                    assert_true("Name should be greater or equal to last interval", check->name >= last_name);
                } else {
                    assert_true("Start should be greater than last interval", check->start > last_start);
                }
            } else {
                assert_true("End should be greater than last interval", check->end > last_end);
            }
        }

        last_end = check->end;
        last_start = check->start;
        last_name = check->name;
    }

    teardown();
}

void test_pool_iterator(void) {
    interval add, *intv;
    interval_node *check;
    int i;
    pool_iterator pit;
    setup();

    // just initialize an empty map
    add.map = EMPTY_MAP;

    // add some intervals to p
    for (i = 1; i < 4; i++) {
        add.name = i;
        add.start = i * 10;
        add.end = i * 100;
        add_interval(&p, &add);
    }

    // make sure adding the intervals sets the linked list up right
    assert_int_equals("pool start wrong", 0, p.start);
    assert_int_equals("pool end wrong", 2, p.end);
    check = &p.intervals[0];
    assert_int_equals("interval prior wrong", END_OF_POOL, check->prior);
    assert_int_equals("interval next wrong", 1, check->next);
    check = &p.intervals[1];
    assert_int_equals("interval prior wrong", 0, check->prior);
    assert_int_equals("interval next wrong", 2, check->next);
    check = &p.intervals[2];
    assert_int_equals("interval prior wrong", 1, check->prior);
    assert_int_equals("interval next wrong", END_OF_POOL, check->next);

    get_pool_iterator(&p, &pit);
    assert_int_equals("Current is wrong", p.start, pit.current);
    i = 0;
    while (has_next_interval(&pit)) {
        intv = next_interval(&pit);
        check = &p.intervals[i++];

        assert_int_equals("name wrong", check->i.name, intv->name);
        assert_int_equals("start wrong", check->i.start, intv->start);
        assert_int_equals("end wrong", check->i.end, intv->end);
    }
    assert_int_equals("Looped wrong number of times", 3, i);

    p.intervals[0].next = 2;
    p.intervals[2].prior = 0;

    get_pool_iterator(&p, &pit);
    assert_int_equals("Current is wrong", p.start, pit.current);
    i = 0;
    while (has_next_interval(&pit)) {
        intv = next_interval(&pit);
        check = &p.intervals[i++];
        if (i == 2) {
            check = &p.intervals[i++];
        }

        assert_int_equals("name wrong", check->i.name, intv->name);
        assert_int_equals("start wrong", check->i.start, intv->start);
        assert_int_equals("end wrong", check->i.end, intv->end);
    }
    assert_int_equals("Looped wrong number of times", 3, i);

    teardown();
}

// this is used to reset the pool during test_purge_pool
static void prepare_pool(void) {
    interval add;
    int i;
    map_key k;
    map_value v;

    clear_pool(&p);

    // we need a non-empty map
    initialize_map(&add.map);
    k = 1;

    // add some intervals to p
    for (i = 1; i < 4; i++) {
        add.name = i;
        add.start = i * 10;
        add.end = i * 100;
        v.type = integer_type;
        v.integer_value = i * 1000;
        map_set(&add.map, k, &v);

        add_interval(&p, &add);
    }
    destroy_map(&add.map);

    // check that the pool is sane
    assert_int_equals("pool space is wrong", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong", 3, p.size);
    assert_int_equals("pool start is wrong", 0, p.start);
    assert_int_equals("pool end is wrong", 2, p.end);
    assert_int_equals("pool removed is wrong", 0, p.removed);
    assert_not_null("pool intervals should not be null", p.intervals);
}

void test_purge_pool(void) {
    interval *check;
    pool_iterator pit;
    map_value check_value;
    map_key k;
    setup();

    // just set the map key once
    k = 1;

    // set up the pool
    prepare_pool();

    // remove the first item
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    // check that the pool is still sane
    assert_int_equals("pool space is wrong after remove first", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after remove first", 3, p.size);
    assert_int_equals("pool start is wrong after remove first", 1, p.start);
    assert_int_equals("pool end is wrong after remove first", 2, p.end);
    assert_int_equals("pool removed is wrong after remove first", 1, p.removed);

    // purge
    purge_pool(&p);

    // check the pool state
    assert_int_equals("pool space is wrong after first purge", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after first purge", 2, p.size);
    assert_int_equals("pool start is wrong after first purge", 0, p.start);
    assert_int_equals("pool end is wrong after first purge", 1, p.end);
    assert_int_equals("pool removed is wrong after first purge", 0, p.removed);

    // now check that everything is where it should be
    check = &p.intervals[0].i;
    assert_int_equals("starting name is wrong after first purge", 2, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("starting map is wrong after first purge", 2000, check_value.integer_value);

    check = &p.intervals[1].i;
    assert_int_equals("second name is wrong after first purge", 3, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("second map is wrong after first purge", 3000, check_value.integer_value);

    // ---------------------------------------------------------------
    // set up the pool
    prepare_pool();

    // remove the middle item
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    // check that the pool is still sane
    assert_int_equals("pool space is wrong after remove middle", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after remove middle", 3, p.size);
    assert_int_equals("pool start is wrong after remove middle", 0, p.start);
    assert_int_equals("pool end is wrong after remove middle", 2, p.end);
    assert_int_equals("pool removed is wrong after remove middle", 1, p.removed);

    // purge
    purge_pool(&p);

    // check the pool state
    assert_int_equals("pool space is wrong after middle purge", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after middle purge", 2, p.size);
    assert_int_equals("pool start is wrong after middle purge", 0, p.start);
    assert_int_equals("pool end is wrong after middle purge", 1, p.end);
    assert_int_equals("pool removed is wrong after middle purge", 0, p.removed);

    // now check that everything is where it should be
    check = &p.intervals[0].i;
    assert_int_equals("starting name is wrong after middle purge", 1, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("starting map is wrong after middle purge", 1000, check_value.integer_value);

    check = &p.intervals[1].i;
    assert_int_equals("second name is wrong after middle purge", 3, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("second map is wrong after middle purge", 3000, check_value.integer_value);


    // ---------------------------------------------------------------
    // set up the pool
    prepare_pool();

    // remove the last item
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    next_interval(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    // check that the pool is still sane
    assert_int_equals("pool space is wrong after remove last", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after remove last", 3, p.size);
    assert_int_equals("pool start is wrong after remove last", 0, p.start);
    assert_int_equals("pool end is wrong after remove last", 1, p.end);
    assert_int_equals("pool removed is wrong after remove last", 1, p.removed);

    // purge
    purge_pool(&p);

    // check the pool state
    assert_int_equals("pool space is wrong after last purge", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after last purge", 2, p.size);
    assert_int_equals("pool start is wrong after last purge", 0, p.start);
    assert_int_equals("pool end is wrong after last purge", 1, p.end);
    assert_int_equals("pool removed is wrong after last purge", 0, p.removed);

    // now check that everything is where it should be
    check = &p.intervals[0].i;
    assert_int_equals("starting name is wrong after last purge", 1, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("starting map is wrong after last purge", 1000, check_value.integer_value);

    check = &p.intervals[1].i;
    assert_int_equals("second name is wrong after last purge", 2, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("second map is wrong after last purge", 2000, check_value.integer_value);

    // ---------------------------------------------------------------
    // set up the pool
    prepare_pool();

    // remove the last two items
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    // check that the pool is still sane
    assert_int_equals("pool space is wrong after remove last two", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after remove last two", 3, p.size);
    assert_int_equals("pool start is wrong after remove last two", 0, p.start);
    assert_int_equals("pool end is wrong after remove last two", 0, p.end);
    assert_int_equals("pool removed is wrong after remove last two", 2, p.removed);

    // purge
    purge_pool(&p);

    // check the pool state
    assert_int_equals("pool space is wrong after last two purge", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after last two purge", 1, p.size);
    assert_int_equals("pool start is wrong after last two purge", 0, p.start);
    assert_int_equals("pool end is wrong after last two purge", 0, p.end);
    assert_int_equals("pool removed is wrong after last two purge", 0, p.removed);

    // now check that everything is where it should be
    check = &p.intervals[0].i;
    assert_int_equals("starting name is wrong after last two purge", 1, check->name);
    map_get(&check->map, k, &check_value);
    assert_int_equals("starting map is wrong after last two purge", 1000, check_value.integer_value);

    // ---------------------------------------------------------------
    // set up the pool
    prepare_pool();

    // remove the all the items
    get_pool_iterator(&p, &pit);
    next_interval(&pit);
    remove_from_pool(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);
    next_interval(&pit);
    remove_from_pool(&pit);

    // check that the pool is still sane
    assert_int_equals("pool space is wrong after remove all", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after remove all", 3, p.size);
    assert_int_equals("pool start is wrong after remove all", END_OF_POOL, p.start);
    assert_int_equals("pool end is wrong after remove all", END_OF_POOL, p.end);
    assert_int_equals("pool removed is wrong after remove all", 3, p.removed);

    // purge
    purge_pool(&p);

    // check the pool state
    assert_int_equals("pool space is wrong after all purge", INITIAL_POOL_SIZE, p.space);
    assert_int_equals("pool size is wrong after all purge", 0, p.size);
    assert_int_equals("pool start is wrong after all purge", END_OF_POOL, p.start);
    assert_int_equals("pool end is wrong after all purge", END_OF_POOL, p.end);
    assert_int_equals("pool removed is wrong after all purge", 0, p.removed);

    teardown();
}
