/*
 * test_semantic.h
 *
 *  Created on: Sep 9, 2019
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

#ifndef TEST_INC_TEST_SEMANTIC_H_
#define TEST_INC_TEST_SEMANTIC_H_

void test_set_field_mapping_per_rule(void);
void test_set_time_mapping_per_rule(void);
void test_remap_field_or_time_mappings(void);
void test_expr_references_ie(void);
void test_remap_nested_boolean(void);
void test_remap_field_complex(void);
void test_set_map_boolean_type(void);

/* these are for normally static functions in semantic.c */
#include "types.h"
#include "ast.h"
#include "dict.h"
#include "map.h"
bool set_field_mapping_per_rule(ast_node *, dictionary *, word_id, map_key, map_key *, side_enum *, bool, bool);
bool set_time_mapping_per_rule(ast_node *, dictionary *, word_id, map_key *, side_enum *, bool *, int, bool, bool);
bool remap_field_or_time_mappings(ast_node *, ast_node *, dictionary *, bool is_where_expr);
bool expr_references_ie(ast_node *, ast_node *);
void set_map_boolean_type(ast_node *node, bool subfield);

#endif /* TEST_INC_TEST_SEMANTIC_H_ */
