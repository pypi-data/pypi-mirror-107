/*
 * strings.h
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

#ifndef INC_STRINGS_H_
#define INC_STRINGS_H_

#include <stdint.h>
#include "types.h"

void copy_string(char *, const char *, int);
bool string_equals(const char *, const char *, int);
int string_length(const char *, int);
uint64_t string_to_u64(const char *, int);
int64_t string_to_i64(const char *, int);
double string_to_double(const char *, int);

#endif /* INC_STRINGS_H_ */
