/*
 * test_string.h
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

#ifndef TEST_INC_TEST_STRINGS_H_
#define TEST_INC_TEST_STRINGS_H_

void test_copy_string(void);
void test_string_equals(void);
void test_string_length(void);
void test_string_to_u64(void);
void test_string_to_i64(void);
void test_string_to_double(void);

#endif /* TEST_INC_TEST_STRINGS_H_ */
