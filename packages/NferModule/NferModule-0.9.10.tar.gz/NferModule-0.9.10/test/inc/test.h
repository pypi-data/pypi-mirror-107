/*
 * test.h
 *
 *  Created on: Apr 5, 2012
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

#ifndef TEST_H_
#define TEST_H_

#include "types.h"

void test_runner(void (*test)(void), const char *name);
void assert_true(char *msg, bool val);
void assert_false(char *msg, bool val);
void assert_null(char *msg, void *val);
void assert_not_null(char *msg, void *val);
void assert_str_equals(char *msg, char *val0, char *val1);
void assert_int_equals(char *msg, unsigned long long val0, unsigned long long val1);
void assert_ptr_equals(char *msg, void *val0, void *val1);
void assert_float_equals(char *msg, double val0, double val1);

#endif /* TEST_H_ */
