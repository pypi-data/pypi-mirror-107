/*
 * test_semantic.c
 *
 *  Created on: September 9, 2019
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

#include "types.h"
#include "ast.h"
#include "semantic.h"
#include "dsl.tab.h"
#include "test_semantic.h"
#include "test.h"
#include "log.h"

static const char *a_str = "a", *b_str = "b", *c_str = "c", *d_str = "d", *x1_str = "x1",
    *foo_str = "foo", *bar_str = "bar", *x_str = "x", *y_str = "y", *boo_str = "boo";
static dictionary parser_dict, label_dict, name_dict, key_dict;
static ast_node *a_before_x1, *b_before_c;
static ast_node *a_foo_eq_b_foo, *a_foo, *b_foo, *a_bar, *b_begin, *a_bar_eq_b_begin, *b_boo;
static ast_node *a_x, *a_y, *b_y1, *b_y2, *c_y, *b_y_eq_c_y, *a_x_and_eq, *a_y_eq_b_y, *and_and_eq;
static word_id a_name, b_name, c_name, x1_name;
static word_id a_lab, b_lab, c_lab;
static word_id foo_key, bar_key, x_key, y_key, boo_key;
static location_type EMPTY_LOCATION = (location_type){0, 0, 0, 0};

static void mock_parse(void) {
    word_id a_id, b_id, c_id, foo_id, bar_id, x_id, y_id, boo_id;
    ast_node *a_node, *b_node, *c_node;

    // pretend to be the parser for interval expression a before (b before c)
    initialize_dictionary(&parser_dict);
    a_id = add_word(&parser_dict, a_str);
    b_id = add_word(&parser_dict, b_str);
    c_id = add_word(&parser_dict, c_str);
    add_word(&parser_dict, d_str);

    a_node = new_atomic_interval_expr(WORD_NOT_FOUND, a_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_node = new_atomic_interval_expr(WORD_NOT_FOUND, b_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    c_node = new_atomic_interval_expr(WORD_NOT_FOUND, c_id, &EMPTY_LOCATION, &EMPTY_LOCATION);

    b_before_c = new_binary_interval_expr(BEFORE, false, b_node, c_node);
    a_before_x1 = new_binary_interval_expr(BEFORE, false, a_node, b_before_c);

    // now pretend to be the parser for the expr a.foo = b.foo
    foo_id = add_word(&parser_dict, foo_str);
    a_foo = new_map_field(a_id, foo_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_foo = new_map_field(b_id, foo_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    a_foo_eq_b_foo = new_binary_expr(EQ, a_foo, b_foo);

    // pretend to parse the expr a.bar = b.begin
    bar_id = add_word(&parser_dict, bar_str);
    a_bar = new_map_field(a_id, bar_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_begin = new_time_field(BEGINTOKEN, b_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    a_bar_eq_b_begin = new_binary_expr(EQ, a_bar, b_begin);

    // pretend to parse the expr (a.x & (b.y = c.y)) & (a.y = b.y)
    x_id = add_word(&parser_dict, x_str);
    y_id = add_word(&parser_dict, y_str);
    a_x = new_map_field(a_id, x_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    a_y = new_map_field(a_id, y_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_y1 = new_map_field(b_id, y_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_y2 = new_map_field(b_id, y_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    c_y = new_map_field(c_id, y_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
    b_y_eq_c_y = new_binary_expr(EQ, b_y1, c_y);
    a_x_and_eq = new_binary_expr(AND, a_x, b_y_eq_c_y);
    a_y_eq_b_y = new_binary_expr(EQ, a_y, b_y2);
    and_and_eq = new_binary_expr(AND, a_x_and_eq, a_y_eq_b_y);

    // pretend to parse the expr b.boo
    boo_id = add_word(&parser_dict, boo_str);
    b_boo = new_map_field(b_id, boo_id, &EMPTY_LOCATION, &EMPTY_LOCATION);
}
static void mock_determine_labels(void) {
    map_value bie_value;

    // now set up the other data structures from semantic analysis
    // this one sets up the binary interval expressions
    initialize_dictionary(&label_dict);
    initialize_dictionary(&name_dict);
    a_lab = add_word(&label_dict, a_str);
    b_lab = add_word(&label_dict, b_str);
    c_lab = add_word(&label_dict, c_str);
    a_name = add_word(&name_dict, a_str);
    b_name = add_word(&name_dict, b_str);
    c_name = add_word(&name_dict, c_str);
    x1_name = add_word(&name_dict, x1_str);

    initialize_map(&b_before_c->binary_interval_expr.left_label_map);
    initialize_map(&b_before_c->binary_interval_expr.right_label_map);
    initialize_map(&b_before_c->binary_interval_expr.left_field_map);
    initialize_map(&b_before_c->binary_interval_expr.right_field_map);

    initialize_map(&a_before_x1->binary_interval_expr.left_label_map);
    initialize_map(&a_before_x1->binary_interval_expr.right_label_map);
    initialize_map(&a_before_x1->binary_interval_expr.left_field_map);
    initialize_map(&a_before_x1->binary_interval_expr.right_field_map);

    bie_value.type = pointer_type;
    bie_value.pointer_value = b_before_c;
    map_set(&b_before_c->binary_interval_expr.left_label_map, b_lab, &bie_value);
    b_before_c->binary_interval_expr.left_name = b_name;
    map_set(&b_before_c->binary_interval_expr.right_label_map, c_lab, &bie_value);
    b_before_c->binary_interval_expr.right_name = c_name;

    bie_value.pointer_value = a_before_x1;
    map_set(&a_before_x1->binary_interval_expr.left_label_map, a_lab, &bie_value);
    b_before_c->binary_interval_expr.left_name = b_name;
    map_set(&a_before_x1->binary_interval_expr.right_label_map, b_lab, &bie_value);
    map_set(&a_before_x1->binary_interval_expr.right_label_map, c_lab, &bie_value);
    b_before_c->binary_interval_expr.right_name = x1_name;
}
static void mock_set_subfields(void) {
    // set the is_subfield field on map fields

    // first for a.foo = b.foo
    b_foo->map_field.is_non_boolean = true;
    a_foo->map_field.is_non_boolean = true;

    // then for a.bar = b.begin
    a_bar->map_field.is_non_boolean = true;

    // then for (a.x & (b.y = c.y)) & (a.y = b.y)
    a_x->map_field.is_non_boolean = false;
    b_y1->map_field.is_non_boolean = true;
    c_y->map_field.is_non_boolean = true;
    a_y->map_field.is_non_boolean = true;
    b_y2->map_field.is_non_boolean = true;

    // then for b.boo
    b_boo->map_field.is_non_boolean = false;
}
static void mock_determine_fields(void) {
    // again, pretend to do the semantic analysis
    initialize_dictionary(&key_dict);
    // first for a.foo = b.foo
    foo_key = add_word(&key_dict, foo_str);
    b_foo->map_field.resulting_map_key = foo_key;
    b_foo->map_field.interval_expression = b_before_c;
    b_foo->map_field.resulting_label_id = b_lab;
    a_foo->map_field.resulting_map_key = foo_key;
    a_foo->map_field.interval_expression = a_before_x1;
    a_foo->map_field.resulting_label_id = a_lab;

    a_foo_eq_b_foo->binary_expr.belongs_in = a_before_x1;

    // then for a.bar = b.begin
    bar_key = add_word(&key_dict, bar_str);
    b_begin->time_field.interval_expression = b_before_c;
    b_begin->time_field.resulting_label_id = b_lab;
    a_bar->map_field.resulting_map_key = bar_key;
    a_bar->map_field.interval_expression = a_before_x1;
    a_bar->map_field.resulting_label_id = a_lab;

    a_bar_eq_b_begin->binary_expr.belongs_in = a_before_x1;

    // then for (a.x & (b.y = c.y)) & (a.y = b.y)
    x_key = add_word(&key_dict, x_str);
    y_key = add_word(&key_dict, y_str);
    a_x->map_field.resulting_map_key = x_key;
    a_x->map_field.interval_expression = a_before_x1;
    a_x->map_field.resulting_label_id = a_lab;
    a_y->map_field.resulting_map_key = y_key;
    a_y->map_field.interval_expression = a_before_x1;
    a_y->map_field.resulting_label_id = a_lab;
    b_y1->map_field.resulting_map_key = y_key;
    b_y1->map_field.interval_expression = b_before_c;
    b_y1->map_field.resulting_label_id = b_lab;
    b_y2->map_field.resulting_map_key = y_key;
    b_y2->map_field.interval_expression = b_before_c;
    b_y2->map_field.resulting_label_id = b_lab;
    c_y->map_field.resulting_map_key = y_key;
    c_y->map_field.interval_expression = b_before_c;
    c_y->map_field.resulting_label_id = c_lab;

    b_y_eq_c_y->binary_expr.belongs_in = b_before_c;
    a_x_and_eq->binary_expr.belongs_in = a_before_x1;
    a_y_eq_b_y->binary_expr.belongs_in = a_before_x1;
    and_and_eq->binary_expr.belongs_in = NULL;

    // then for b.boo
    boo_key = add_word(&key_dict, boo_str);
    b_boo->map_field.resulting_map_key = boo_key;
    b_boo->map_field.interval_expression = b_before_c;
    b_boo->map_field.resulting_label_id = b_lab;
}

static void teardown(void) {
    free_node(a_before_x1);
    free_node(a_foo_eq_b_foo);
    free_node(a_bar_eq_b_begin);
    free_node(and_and_eq);
    free_node(b_boo);
    destroy_dictionary(&parser_dict);
    destroy_dictionary(&label_dict);
    destroy_dictionary(&name_dict);
    destroy_dictionary(&key_dict);
}

void test_set_field_mapping_per_rule(void) {
    map_key result;
    side_enum side;
    int dict_size;
    map_value value;
    word_id mapped_word;

    /* basic test: there is a rule with two BIEs, and the top level rule includes an expression which references the bottom one.
     * d :- a before (b before c) where a.foo = b.foo
     * What should happen: lower rule gets a mapping for b.foo to a new key and top rule gets set to reference it.
     */
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // store key dict size
    dict_size = key_dict.size;

    // setup does most of the work
    // call the function for a.foo
    set_field_mapping_per_rule(
            a_before_x1, // the interval expression where the field will be used
            &key_dict, // the key dictionary
            a_lab,    // the label of the interval to reference
            foo_key,  // the key of the field
            &result,  // where the field key should be stored
            &side,    // where the side of the key should be stored
            true,     // exclusion is okay because this is a where clause
            false     // always false when the function is called
            );

    // verify that the key_dict remains the same
    assert_int_equals("Key dict should not have been changed", dict_size, key_dict.size);

    // verify the correct values for result and side
    assert_str_equals("Wrong key returned for a.foo field mapping", get_word(&key_dict, foo_key), get_word(&key_dict, result));
    assert_int_equals("Wrong side returned for a.foo field mapping", left_side, side);

    // now do the b.foo field
    set_field_mapping_per_rule(
            a_before_x1, // the interval expression where the field will be used
            &key_dict, // the key dictionary
            b_lab,    // the label of the interval to reference
            foo_key,  // the key of the field
            &result,  // where the field key should be stored
            &side,    // where the side of the key should be stored
            true,     // exclusion is okay because this is a where clause
            false     // always false when the function is called
            );

    // verify that the key_dict increased by one
    assert_int_equals("Key dict should have been changed", dict_size + 1, key_dict.size);

    // this is abusing the implementation.  We assume we know that the new key will be "F_foo-0".
    mapped_word = find_word(&key_dict, "F_foo-0");
    // verify the correct values for result and side
    // use strings for better failure reporting
    assert_str_equals("Wrong key returned for b.foo field mapping", "F_foo-0", get_word(&key_dict, result));
    assert_int_equals("Wrong side returned for b.foo field mapping", right_side, side);

    // we also need to check that the map was updated on the lower bie
    map_get(&b_before_c->binary_interval_expr.left_field_map, mapped_word, &value);
    assert_int_equals("A mapping should be created for b.foo", string_type, value.type);
    assert_int_equals("foo field should be mapped on b before c", foo_key, value.string_value);

    teardown();
}

void test_set_time_mapping_per_rule(void) {
    map_key result;
    side_enum side;
    int dict_size;
    bool is_time;
    word_id mapped_word;

    /* basic test: there is a rule with two BIEs, and the top level rule includes an expression which references the bottom one.
     * d :- a before (b before c) where a.bar = b.begin
     * What should happen: lower rule gets a mapping for b.begin to a new key and top rule gets set to reference it.
     */
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // store key dict size
    dict_size = key_dict.size;

    // setup does most of the work
    // do the b.begin time field
    set_time_mapping_per_rule(
            a_before_x1, // the interval expression where the field will be used
            &key_dict, // the key dictionary
            b_lab,    // the label of the interval to reference
            &result,  // where the field key should be stored
            &side,    // where the side of the key should be stored
            &is_time, // returns if the time field is still a time field or not
            BEGINTOKEN, // the time field in question
            true,     // exclusion is okay because this is a where clause
            false     // always false when the function is called
            );

    // verify that the key_dict increased by one
    assert_int_equals("Key dict should have been changed", dict_size + 1, key_dict.size);

    // this is abusing the implementation.  We assume we know that the new key will be F_BEGIN-0.
    mapped_word = find_word(&key_dict, "F_BEGIN-0");
    // verify the correct values for result and side
    // use strings for better failure reporting
    assert_str_equals("Wrong key returned for b.begin time mapping", "F_BEGIN-0", get_word(&key_dict, result));
    assert_int_equals("Wrong side returned for b.begin time mapping", right_side, side);
    // check is_time
    assert_false("Time field should not be time", is_time);

    // we also need to check that the map was created on the lower bie
    assert_int_equals("A mapping should be created for b.begin", mapped_word, b_before_c->binary_interval_expr.left_begin_map);
    assert_int_equals("No mapping should be created for b.end", WORD_NOT_FOUND, b_before_c->binary_interval_expr.left_end_map);
    assert_int_equals("No mapping should be created for c.begin", WORD_NOT_FOUND, b_before_c->binary_interval_expr.right_end_map);
    assert_int_equals("No mapping should be created for c.end", WORD_NOT_FOUND, b_before_c->binary_interval_expr.right_end_map);

    // try a somewhat more complex rule
    // (a.x & (b.y = c.y)) & (a.y = b.y)

    teardown();
}

void test_remap_field_or_time_mappings(void) {
    int dict_size;
    word_id mapped_word;
    map_value value;

    /* basic test: there is a rule with two BIEs, and the top level rule includes an expression which references the bottom one.
     * d :- a before (b before c) where a.foo = b.foo
     * What should happen: lower rule gets a mapping for b.foo to a new key and top rule gets set to reference it.
     */
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // store key dict size
    dict_size = key_dict.size;
    // call remap for the top level rule and the node that references its child
    remap_field_or_time_mappings(a_before_x1, b_foo, &key_dict, true);

    // verify that the key_dict increased by one
    assert_int_equals("Key dict should have been changed", dict_size + 1, key_dict.size);

    // check the results
    mapped_word = find_word(&key_dict, "F_foo-0");
    assert_int_equals("Should have remapped b.foo to x1.F_foo-0", mapped_word, b_foo->map_field.resulting_map_key);
    // we also need to check that the map was updated on the lower bie
    map_get(&b_before_c->binary_interval_expr.left_field_map, mapped_word, &value);
    assert_int_equals("A mapping should be created for b.foo", string_type, value.type);
    assert_int_equals("foo field should be mapped on b before c", foo_key, value.string_value);

    // call remap for the top level rule and the node that references its child
    remap_field_or_time_mappings(a_before_x1, b_begin, &key_dict, true);

    // verify that the key_dict increased again
    assert_int_equals("Key dict should have been changed", dict_size + 2, key_dict.size);

    // check the results
    mapped_word = find_word(&key_dict, "F_BEGIN-0");
    // verify the correct values for result and side
    assert_int_equals("Should have remapped b.begin to x1.F_BEGIN-0", mapped_word, b_begin->time_field.resulting_map_key);
    assert_false("Time field should not be time", b_begin->time_field.is_time);

    // we also need to check that the map was created on the lower bie
    assert_int_equals("A mapping should be created for b.begin", mapped_word, b_before_c->binary_interval_expr.left_begin_map);
    assert_int_equals("No mapping should be created for b.end", WORD_NOT_FOUND, b_before_c->binary_interval_expr.left_end_map);
    assert_int_equals("No mapping should be created for c.begin", WORD_NOT_FOUND, b_before_c->binary_interval_expr.right_end_map);
    assert_int_equals("No mapping should be created for c.end", WORD_NOT_FOUND, b_before_c->binary_interval_expr.right_end_map);

    teardown();
}

void test_remap_nested_boolean(void) {
    int dict_size;

    /* test with a single nested boolean: there is a rule with two BIEs, and the only restriction is on the nested rule.
     * d :- a before (b before c) where b.boo
     * What should happen: the lower rule references the field and no remapping is performed.
     */
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // store key dict size
    dict_size = key_dict.size;
    // call remap for the top level rule and the node that references its child
    remap_field_or_time_mappings(a_before_x1, b_boo, &key_dict, true);

    // verify that the key_dict did not change
    assert_int_equals("Key dict should not have been changed", dict_size, key_dict.size);

    // check the results
    assert_int_equals("Should not have remapped b.boo", boo_key, b_boo->map_field.resulting_map_key);

    // we also need to check that the map on the lower bie was not changed
    assert_true("The map on b before c should not have been changed", is_map_empty(&b_before_c->binary_interval_expr.left_field_map));

    teardown();
}

void test_remap_field_complex(void) {
    int dict_size;
    word_id mapped_word;
    map_value value;

    /* complex test: there's a rule with a complex where expr: (a.x & (b.y = c.y)) & (a.y = b.y)
     * What should happen: lower rule gets a mapping for b.y to a new key and only the correct field is set to reference it.
     * bies are traversed bottom-up, left-to-right
     * exprs are also traversed bottom-up, left-to-right
     */
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // store key dict size
    dict_size = key_dict.size;

    /*
     * order:
     * 1. check b_before_c with (b.y = c.y) -> both sides refer
     *   1a. left references exact, so skip
     *   1b. right references exact, so skip
     * 2. check b_before_c with (a_x & (b.y = c.y)) -> left doesn't refer
     * 3. check b_before_c with (a.y = b.y) -> left doesn't refer
     * 4. check b_before_c with (a.x & (b.y = c.y)) & (a.y = b.y) -> neither side refers
     * 5. check a_before_x1 with (b.y = c.y) -> reference already set
     * 6. check a_before_x1 with (a_x & (b.y = c.y)) -> refers
     *   6a. left references exact, so skip
     *   6b. right doesn't reference exact, so call --  it should do nothing because reference is set
     * 7. check a_before_x1 with (a.y = b.y) -> refers
     *   7a. left references exact, so skip
     *   7b. right doesn't reference exact, so call -- it should remap b.y
     * 8. check a_before_x1 with (a.x & (b.y = c.y)) & (a.y = b.y) -> neither side refers
     */

    // call remap for 6b.
    // this should result in nothing being remapped, since b.y = c.y is already mapped to a nested bie
    remap_field_or_time_mappings(a_before_x1, b_y_eq_c_y, &key_dict, true);

    // verify that the key_dict did not increase
    assert_int_equals("Key dict should not have been changed", dict_size, key_dict.size);

    // check the results
    assert_int_equals("Should not have remapped a.x", x_key, a_x->map_field.resulting_map_key);
    assert_int_equals("Should not have remapped b.y", y_key, b_y1->map_field.resulting_map_key);
    assert_int_equals("Should not have remapped c.y", y_key, c_y->map_field.resulting_map_key);

    // we also need to check that the map was left unchanged
    assert_true("Map should not have been altered", is_map_empty(&b_before_c->binary_interval_expr.left_field_map));

    // call remap for 7b.
    // this should result in b.y being remapped for use in a before x1
    remap_field_or_time_mappings(a_before_x1, b_y2, &key_dict, true);

    // verify that the key_dict was increased by one
    assert_int_equals("Key dict should have been added to", dict_size + 1, key_dict.size);

    // check the results
    mapped_word = find_word(&key_dict, "F_y-0");
    assert_int_equals("Should have remapped b.y to x1.F_y-0", mapped_word, b_y2->map_field.resulting_map_key);
    // we also need to check that the map was updated on the lower bie
    map_get(&b_before_c->binary_interval_expr.left_field_map, mapped_word, &value);
    assert_int_equals("A mapping should be created for b.y", string_type, value.type);
    assert_int_equals("y field should be mapped on b before c", y_key, value.string_value);

    teardown();
}

void test_expr_references_ie(void) {
    mock_parse();
    mock_determine_labels();
    mock_set_subfields();
    mock_determine_fields();

    // test all combinations of expr_references_bie for the rule "a before (b before c) where a.foo = b.foo"
    assert_true("a.foo should reference a before x1", expr_references_ie(a_before_x1, a_foo));
    assert_true("b.foo should reference a before x1", expr_references_ie(a_before_x1, b_foo));
    assert_false("a.foo = b.foo should not reference a before x1", expr_references_ie(a_before_x1, a_foo_eq_b_foo));
    assert_false("a.foo should not reference b before c", expr_references_ie(b_before_c, a_foo));
    assert_true("b.foo should reference b before c", expr_references_ie(b_before_c, b_foo));
    assert_false("a.foo = b.foo should not reference b before c", expr_references_ie(b_before_c, a_foo_eq_b_foo));

    // test all combinations of expr_references_bie for the rule "a before (b before c) where a.bar = b.begin"
    assert_true("a.bar should reference a before x1", expr_references_ie(a_before_x1, a_bar));
    assert_true("b.begin should reference a before x1", expr_references_ie(a_before_x1, b_begin));
    assert_false("a.bar = b.begin should not reference a before x1", expr_references_ie(a_before_x1, a_bar_eq_b_begin));
    assert_false("a.bar should not reference b before c", expr_references_ie(b_before_c, a_bar));
    assert_true("b.begin should reference b before c", expr_references_ie(b_before_c, b_begin));
    assert_false("a.bar = b.begin should not reference b before c", expr_references_ie(b_before_c, a_bar_eq_b_begin));

    // test all combinations of expr_references_bie for the rule "a before (b before c) where (a.x & (b.y = c.y)) & (a.y = b.y)"
    assert_true("a.x should reference a before x1", expr_references_ie(a_before_x1, a_x));
    assert_true("b.y1 should reference a before x1", expr_references_ie(a_before_x1, b_y1));
    assert_true("c.y should reference a before x1", expr_references_ie(a_before_x1, c_y));
    assert_true("a.y should reference a before x1", expr_references_ie(a_before_x1, a_y));
    assert_true("b.y2 should reference a before x1", expr_references_ie(a_before_x1, b_y2));
    assert_true("b.y = c.y should reference a before x1", expr_references_ie(a_before_x1, b_y_eq_c_y));
    assert_false("a.x & (b.y = c.y) should not reference a before x1", expr_references_ie(a_before_x1, a_x_and_eq));
    assert_false("a.y = b.y should not reference a before x1", expr_references_ie(a_before_x1, a_y_eq_b_y));
    assert_false("(a.x & (b.y = c.y)) & (a.y = b.y) should not reference a before x1", expr_references_ie(a_before_x1, and_and_eq));

    assert_false("a.x should not reference b before c", expr_references_ie(b_before_c, a_x));
    assert_true("b.y1 should reference b before c", expr_references_ie(b_before_c, b_y1));
    assert_true("c.y should reference b before c", expr_references_ie(b_before_c, c_y));
    assert_false("a.y should not reference b before c", expr_references_ie(b_before_c, a_y));
    assert_true("b.y2 should reference b before c", expr_references_ie(b_before_c, b_y2));
    assert_true("b.y = c.y should reference b before c", expr_references_ie(b_before_c, b_y_eq_c_y));
    assert_false("a.x & (b.y = c.y) should not reference b before c", expr_references_ie(b_before_c, a_x_and_eq));
    assert_false("a.y = b.y should not reference b before c", expr_references_ie(b_before_c, a_y_eq_b_y));
    assert_false("(a.x & (b.y = c.y)) & (a.y = b.y) should not reference b before c", expr_references_ie(b_before_c, and_and_eq));

    // test all combinations of expr_references_bie for the rule "a before (b before c) where b.boo"
    assert_true("b.boo should reference a before x1", expr_references_ie(a_before_x1, b_boo));
    assert_true("b.boo should reference b before c", expr_references_ie(b_before_c, b_boo));

    teardown();
}

void test_set_map_boolean_type(void) {
    mock_parse();
    mock_determine_labels();

    // verify that all the is_subfield fields are set correctly

    // first for a.foo = b.foo
    set_map_boolean_type(a_foo_eq_b_foo, false);
    // check the fields
    assert_true("a.foo is a subfield of a non-Boolean", a_foo->map_field.is_non_boolean);
    assert_true("b.foo is a subfield of a non-Boolean", b_foo->map_field.is_non_boolean);

    // then for a.bar = b.begin
    set_map_boolean_type(a_bar_eq_b_begin, false);
    // check the fields
    assert_true("a.bar is a subfield of a non-Boolean", a_bar->map_field.is_non_boolean);

    // then for (a.x & (b.y = c.y)) & (a.y = b.y)
    set_map_boolean_type(and_and_eq, false);
    // check the fields
    assert_false("a.x is not a subfield of a non-Boolean", a_x->map_field.is_non_boolean);
    assert_true("b.y1 is a subfield of a non-Boolean", b_y1->map_field.is_non_boolean);
    assert_true("c.y is a subfield of a non-Boolean", c_y->map_field.is_non_boolean);
    assert_true("a.y is a subfield of a non-Boolean", a_y->map_field.is_non_boolean);
    assert_true("b.y2 is a subfield of a non-Boolean", b_y2->map_field.is_non_boolean);

    // then for b.boo
    set_map_boolean_type(b_boo, false);
    // check the fields
    assert_false("b.boo is not a subfield of a non-Boolean", b_boo->map_field.is_non_boolean);
}
