/*
 * test_pool.h
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

#ifndef TEST_POOL_H_
#define TEST_POOL_H_

void test_initialize_pool(void);
void test_destroy_pool(void);

void test_add_interval(void);
void test_copy_pool(void);
void test_sort_pool(void);
void test_large_ts_sort(void);
void test_pool_iterator(void);
void test_purge_pool(void);


#endif /* TEST_POOL_H_ */
