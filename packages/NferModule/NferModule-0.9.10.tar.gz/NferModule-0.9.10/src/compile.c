/*
 * compile.c
 *
 *  Created on: May 7, 2018
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
#include <inttypes.h>

#include "types.h"
#include "dict.h"
#include "log.h"
#include "map.h"
#include "pool.h"
#include "nfer.h"
#include "ast.h"
#include "generate.h"
#include "expression.h"
#include "stack.h"
#include "dsl.tab.h"
#include "rdc.h"

#define LEFT_START  "s1"
#define LEFT_END    "e1"
#define LEFT_MAP    "m1"
#define RIGHT_START "s2"
#define RIGHT_END   "e2"
#define RIGHT_MAP   "m2"

/**
 * This is all the code brought in from preprocessing with XXD into char arrays.
 */

extern unsigned char gensrc_compiler_headers_h_rdc[];
extern unsigned char gensrc_compiler_srccode_c_rdc[];

/**
 * Write a dictionary as a C file.  The resulting code can be used to load a ready dictionary statically.
 */
static void export_dictionary(char *name, FILE *file, dictionary *dict, char *size_define) {
    dictionary_iterator dit;

    // write a header
    fprintf(file, "/** exported nfer %s dictionary begin **/\n", name);

    // the provided name will be used for namespacing, essentially
    // first statically allocate space for the words and hash
    if (size_define == EXPORT_DICT_USE_SIZE) {
        // if we used 2*space for the hash size the keys would work out the same as in memory.
        // however, at the moment this seems like it isn't necessary and we only need to look up values at
        // initialization time, so I am leaving this as 2*size to save a tiny bit of memory.
        // note that changing has other consequences in this function...
        fprintf(file, "word %s_words[%d];\nword_id %s_hash[%d];\n", name, dict->size, name, dict->size * 2);

        // write the struct
        // space, size, *words, *hash, dynamic
        fprintf(file, "dictionary %s_dict = {%d, 0, %s_words, %s_hash, false};\n", name, dict->size, name, name);
    } else {
        fprintf(file, "word %s_words[%s];\nword_id %s_hash[%s * 2];\n", name, size_define, name, size_define);

        // write the struct
        // space, size, *words, *hash, dynamic
        fprintf(file, "dictionary %s_dict = {%s, 0, %s_words, %s_hash, false};\n", name, size_define, name, name);
    }

    // put the value initialization in an init function named in a predictable way
    fprintf(file, "static void init_%s_dict(void) {\n", name);
    // initialize the memory
    fprintf(file, "    clear_memory(%s_words, sizeof(word) * %s_dict.space);\n", name, name);
    fprintf(file, "    set_memory(%s_hash, sizeof(word_id) * %s_dict.space * 2);\n", name, name);

    get_dictionary_iterator(dict, &dit);
    while (has_next_word(&dit)) {
        // just using add_word simplifies things significantly
        fprintf(file, "    add_word(&%s_dict, \"%s\");\n", name, get_word(dict, next_word(&dit)));
    }
    fprintf(file, "}\n");
}

static void export_expression(char *name, FILE *file, expression_input *input, dictionary *key_dict, dictionary *val_dict) {
    unsigned int position, length;
    expression_action action;

    // length is stored as the first element in the action list
    length = input[0].length;

    position = 1;

    // write a declaration using the length.  C89 doesn't support union initialization with curly braces, so we have
    // to break it out into an init function.
    fprintf(file, "expression_input %s_expression[%d];\n", name, length);

    // write the initialization function start
    fprintf(file, "static void init_%s_expression(dictionary *key_dict, dictionary *val_dict) {\n", name);
    // write the length
    fprintf(file, "    %s_expression[0].length = %d;\n", name, length);

    // now iterate over the rest and write whatever field makes sense
    while (position < length) {
        action = input[position++].action;

        switch(action) {
        case action_add:
        case action_sub:
        case action_mul:
        case action_div:
        case action_mod:
        case action_lt:
        case action_gt:
        case action_lte:
        case action_gte:
        case action_eq:
        case action_ne:
        case action_and:
        case action_or:
        case action_neg:
        case action_not:
        case param_left_begin:
        case param_left_end:
        case param_right_begin:
        case param_right_end:
            // just write the action.  To simplify the code don't bother with readable names.
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            break;

        // for all the literals and fields we have to write extra information after the action
        case param_boollit:
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            fprintf(file, "    %s_expression[%d].boolean_value = %d;\n", name, position, input[position].boolean_value);
            position++;
            break;

        case param_intlit:
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            fprintf(file, "    %s_expression[%d].integer_value = %" PRIu64 ";\n", name, position, input[position].integer_value);
            position++;
            break;

        case param_reallit:
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            fprintf(file, "    %s_expression[%d].real_value = %f;\n", name, position, input[position].real_value);
            position++;
            break;

        case param_strlit:
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            // we have to do the word lookup here
            fprintf(file, "    %s_expression[%d].string_value = find_word(val_dict, \"%s\");\n", name, position, get_word(val_dict, input[position].string_value));
            position++;
            break;

        case param_left_field:
        case param_right_field:
            fprintf(file, "    %s_expression[%d].action = %d;\n", name, position - 1, action);
            // we have to do the word lookup here
            fprintf(file, "    %s_expression[%d].field_name = find_word(key_dict, \"%s\");\n", name, position, get_word(key_dict, input[position].field_name));
            position++;
            break;
        }
    }
    // close it up
    fprintf(file, "}\n");
}

static void export_specification(FILE *file, nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    int num_rules, i;
    nfer_rule *rule;
    char function_name_buffer[MAX_WORD_LENGTH + 1];
    map_iterator mit;
    map_key key;
    map_value map_expression;
    unsigned int stack_depth, max_stack_depth;

    // get the number of rules
    num_rules = spec->rule_list.size;

    // global declarations
    filter_log_msg(LOG_LEVEL_DEBUG, "Writing globals.\n");
    fprintf(file, "nfer_specification global_spec;\n");
    fprintf(file, "rule_id global_left_subscriptions[%d];\nrule_id global_right_subscriptions[%d];\n", name_dict->size, name_dict->size);
    fprintf(file, "nfer_rule global_rule_list[%d];\n", num_rules);

    // set up caches for each rule... maps are the trick
    fprintf(file, "interval_node cache[%d][3][RULE_CACHE_SIZES];\n", spec->rule_list.size);
    fprintf(file, "map_value_node cache_map[%d][3][RULE_CACHE_SIZES][%d];\n", spec->rule_list.size, key_dict->size);
    // set up map expressions
    fprintf(file, "map_value_node map_expression_values[%d][%d];\n", spec->rule_list.size, key_dict->size);
    // we want separate arrays for the new_intervals pool, since it doesn't need to be as big
    fprintf(file, "interval_node new_interval_nodes[%d][NEW_INTERVALS_SIZE];\n", spec->rule_list.size);
    fprintf(file, "map_value_node new_interval_maps[%d][NEW_INTERVALS_SIZE][%d];\n", spec->rule_list.size, key_dict->size);

    // write expression declarations
    for(i = 0; i < num_rules; i++) {
        rule = &spec->rule_list.rules[i];
        max_stack_depth = 0;

        if (rule->where_expression != NULL) {
            snprintf(function_name_buffer, MAX_WORD_LENGTH + 1, "where_%d", i);
            export_expression(function_name_buffer, file, rule->where_expression, key_dict, val_dict);
            stack_depth = max_expression_stack_depth(rule->where_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }
        if (rule->begin_expression != NULL) {
            snprintf(function_name_buffer, MAX_WORD_LENGTH + 1, "begin_%d", i);
            export_expression(function_name_buffer, file, rule->begin_expression, key_dict, val_dict);
            stack_depth = max_expression_stack_depth(rule->begin_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }
        if (rule->end_expression != NULL) {
            snprintf(function_name_buffer, MAX_WORD_LENGTH + 1, "end_%d", i);
            export_expression(function_name_buffer, file, rule->end_expression, key_dict, val_dict);
            stack_depth = max_expression_stack_depth(rule->end_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }

        get_map_iterator(&rule->map_expressions, &mit);
        while (has_next_map_key(&mit)) {
            key = next_map_key(&mit);
            map_get(&rule->map_expressions, key, &map_expression);

            snprintf(function_name_buffer, MAX_WORD_LENGTH + 1, "map_%d_%d", i, key);
            export_expression(function_name_buffer, file, (expression_input *)map_expression.pointer_value, key_dict, val_dict);
            stack_depth = max_expression_stack_depth((expression_input *)map_expression.pointer_value);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }

        // allocate stack values
        if (max_stack_depth > 0) {
            fprintf(file, "stack_value rule_stack_%d[%d];\n", i, max_stack_depth);
        }
    }

    filter_log_msg(LOG_LEVEL_DEBUG, "Writing the spec initialization routine.\n");
    fprintf(file, "static void init_spec(void) {\n");
    // local declarations
    fprintf(file, "    nfer_rule *rule;\n    int i;\n");
    fprintf(file, "    map_value map_expression_value;\n");
    // initialize the spec
    fprintf(file, "    global_spec.subscription_size = %d;\n", name_dict->size);
    fprintf(file, "    global_spec.subscriptions[LEFT_SUBSCRIPTIONS] = global_left_subscriptions;\n");
    fprintf(file, "    global_spec.subscriptions[RIGHT_SUBSCRIPTIONS] = global_right_subscriptions;\n");
    fprintf(file, "    set_memory(global_spec.subscriptions[LEFT_SUBSCRIPTIONS], sizeof(rule_id) * %d);\n", name_dict->size);
    fprintf(file, "    set_memory(global_spec.subscriptions[RIGHT_SUBSCRIPTIONS], sizeof(rule_id) * %d);\n", name_dict->size);
    fprintf(file, "    global_spec.rule_list.space = %d;\n    global_spec.rule_list.size = 0;\n    global_spec.rule_list.rules = global_rule_list;\n", num_rules);
    fprintf(file, "    clear_memory(global_spec.rule_list.rules, sizeof(nfer_rule) * %d);\n", num_rules);
    // zero the caches (we don't need to do this for the stacks)
    fprintf(file, "    clear_memory(cache, %d * 3 * RULE_CACHE_SIZES * sizeof(interval_node));\n", spec->rule_list.size);
    fprintf(file, "    clear_memory(cache_map, %d * 3 * RULE_CACHE_SIZES * %d * sizeof(map_value_node));\n", spec->rule_list.size, key_dict->size);
    // zero the map expressions maps
    fprintf(file, "    clear_memory(map_expression_values, %d * %d * sizeof(map_value_node));\n", spec->rule_list.size, key_dict->size);
    // initialize the static new_interval data structures
    fprintf(file, "    clear_memory(new_interval_nodes, %d * NEW_INTERVALS_SIZE * sizeof(interval_node));\n", spec->rule_list.size);
    fprintf(file, "    clear_memory(new_interval_maps, %d * NEW_INTERVALS_SIZE * %d * sizeof(map_value_node));\n", spec->rule_list.size, key_dict->size);

    // add all the rules to the specification
    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting the rules.\n");
    // call the expression initialization functions and add the rules
    for(i = 0; i < num_rules; i++) {
        rule = &spec->rule_list.rules[i];
        max_stack_depth = 0;

        // add the actual rule first
        if (rule->right_label != WORD_NOT_FOUND) {
            fprintf(file, "    rule = add_rule_to_specification(&global_spec, find_word(&global_name_dict, \"%s\"), find_word(&global_name_dict, \"%s\"), %d, find_word(&global_name_dict, \"%s\"), NULL);\n",
                    get_word(name_dict, rule->result_label),
                    get_word(name_dict, rule->left_label),
                    rule->op_code,
                    get_word(name_dict, rule->right_label));
        } else {
            // needed for atomic rules
            fprintf(file, "    rule = add_rule_to_specification(&global_spec, find_word(&global_name_dict, \"%s\"), find_word(&global_name_dict, \"%s\"), %d, WORD_NOT_FOUND, NULL);\n",
                            get_word(name_dict, rule->result_label),
                            get_word(name_dict, rule->left_label),
                            rule->op_code);
        }
        // set hidden flag
        fprintf(file, "    rule->hidden = %d;\n", rule->hidden);

        // set up new_intervals
        fprintf(file, "    rule->new_intervals.intervals = new_interval_nodes[%d];\n", i);
        fprintf(file, "    rule->new_intervals.space = NEW_INTERVALS_SIZE;\n");
        fprintf(file, "    for (i = 0; i < NEW_INTERVALS_SIZE; i++) {\n");
        fprintf(file, "        rule->new_intervals.intervals[i].i.map.values = new_interval_maps[%d][i];\n", i);
        fprintf(file, "        rule->new_intervals.intervals[i].i.map.space = %d;\n    }\n", key_dict->size);

        // set the caches and set them up
        fprintf(file, "    rule->left_cache.intervals = cache[%d][0];\n", i);
        fprintf(file, "    rule->left_cache.space = RULE_CACHE_SIZES;\n");
        fprintf(file, "    for (i = 0; i < RULE_CACHE_SIZES; i++) {\n");
        fprintf(file, "        rule->left_cache.intervals[i].i.map.values = cache_map[%d][0][i];\n", i);
        fprintf(file, "        rule->left_cache.intervals[i].i.map.space = %d;\n    }\n", key_dict->size);

        fprintf(file, "    rule->right_cache.intervals = cache[%d][1];\n", i);
        fprintf(file, "    rule->right_cache.space = RULE_CACHE_SIZES;\n");
        fprintf(file, "    for (i = 0; i < RULE_CACHE_SIZES; i++) {\n");
        fprintf(file, "        rule->right_cache.intervals[i].i.map.values = cache_map[%d][1][i];\n", i);
        fprintf(file, "        rule->right_cache.intervals[i].i.map.space = %d;\n    }\n", key_dict->size);

        fprintf(file, "    rule->produced.intervals = cache[%d][2];\n", i);
        fprintf(file, "    rule->produced.space = RULE_CACHE_SIZES;\n");
        fprintf(file, "    for (i = 0; i < RULE_CACHE_SIZES; i++) {\n");
        fprintf(file, "        rule->produced.intervals[i].i.map.values = cache_map[%d][2][i];\n", i);
        fprintf(file, "        rule->produced.intervals[i].i.map.space = %d;\n    }\n", key_dict->size);


        // call the expression init functions and assign them
        if (rule->where_expression != NULL) {
            fprintf(file, "    init_where_%d_expression(&global_key_dict, &global_val_dict);\n", i);
            fprintf(file, "    rule->where_expression = where_%d_expression;\n", i);
            stack_depth = max_expression_stack_depth(rule->where_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }
        if (rule->begin_expression != NULL) {
            fprintf(file, "    init_begin_%d_expression(&global_key_dict, &global_val_dict)\n", i);
            fprintf(file, "    rule->begin_expression = begin_%d_expression;\n", i);
            stack_depth = max_expression_stack_depth(rule->begin_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }
        if (rule->end_expression != NULL) {
            fprintf(file, "    init_end_%d_expression(&global_key_dict, &global_val_dict)\n", i);
            fprintf(file, "    rule->end_expression = end_%d_expression;\n", i);
            stack_depth = max_expression_stack_depth(rule->end_expression);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
        }

        // set the map expression values
        fprintf(file, "    rule->map_expressions.values = map_expression_values[%d];\n", i);
        fprintf(file, "    rule->map_expressions.space = %d;\n", key_dict->size);

        get_map_iterator(&rule->map_expressions, &mit);
        while (has_next_map_key(&mit)) {
            key = next_map_key(&mit);
            map_get(&rule->map_expressions, key, &map_expression);

            fprintf(file, "    init_map_%d_%d_expression(&global_key_dict, &global_val_dict);\n", i, key);
            stack_depth = max_expression_stack_depth((expression_input *)map_expression.pointer_value);
            if (stack_depth > max_stack_depth) {
                max_stack_depth = stack_depth;
            }
            // actually assign the map expressions
            fprintf(file, "    map_expression_value.type = pointer_type;\n");
            fprintf(file, "    map_expression_value.pointer_value = map_%d_%d_expression;\n", i, key);
            fprintf(file, "    map_set(&rule->map_expressions, %d, &map_expression_value);\n", key);
        }

        // set the stack values
        if (max_stack_depth > 0) {
            fprintf(file, "    rule->expression_stack.values = rule_stack_%d;\n", i);
            fprintf(file, "    rule->expression_stack.space = %d;\n", max_stack_depth);
        }
    }

    fprintf(file, "}\n");
}

static void export_init(FILE *file, dictionary *key_dict) {
    fprintf(file, "static void init_nfer(void) {\n");
    fprintf(file, "    int i;\n");
    // set nfer options
    fprintf(file, "    opt_full = FULL_RESULTS;\n    opt_window_size = WINDOW_SIZE;\n");
    // for now, enable more logging
    fprintf(file, "    //set_log_level(LOG_LEVEL_DEBUG);\n");
    // initialize the global dictionaries and specification
    fprintf(file, "    init_global_name_dict();\n    init_global_key_dict();\n    init_global_val_dict();\n");
    fprintf(file, "    init_spec();\n");
    // initialize the global i/o
    fprintf(file, "    initialize_pool(&input_pool);\n");
    fprintf(file, "    initialize_pool(&result_pool);\n");
    fprintf(file, "    clear_memory(input_cache, NEW_INTERVALS_SIZE * sizeof(interval_node));\n");
    fprintf(file, "    clear_memory(input_cache_map, NEW_INTERVALS_SIZE * %d * sizeof(map_value_node));\n", key_dict->size);
    fprintf(file, "    input_pool.intervals = input_cache;\n");
    fprintf(file, "    input_pool.space = NEW_INTERVALS_SIZE;\n");
    fprintf(file, "    clear_memory(result_cache, NEW_INTERVALS_SIZE * sizeof(interval_node));\n");
    fprintf(file, "    clear_memory(result_cache_map, NEW_INTERVALS_SIZE * %d * sizeof(map_value_node));\n", key_dict->size);
    fprintf(file, "    result_pool.intervals = result_cache;\n");
    fprintf(file, "    result_pool.space = NEW_INTERVALS_SIZE;\n");
    fprintf(file, "    for (i = 0; i < NEW_INTERVALS_SIZE; i++) {\n");
    fprintf(file, "        input_pool.intervals[i].i.map.values = input_cache_map[i];\n");
    fprintf(file, "        input_pool.intervals[i].i.map.space = %d;\n", key_dict->size);
    fprintf(file, "        result_pool.intervals[i].i.map.values = result_cache_map[i];\n");
    fprintf(file, "        result_pool.intervals[i].i.map.space = %d;\n", key_dict->size);
    fprintf(file, "    }\n");
    fprintf(file, "}\n");

    fprintf(file, "static void wakeup(void) {\n");
    fprintf(file, "    run_nfer(&global_spec, &input_pool, &result_pool);\n");
    fprintf(file, "    output_pool(&result_pool, &global_name_dict, &global_key_dict, &global_val_dict, WRITE_OUTPUT);\n");
    fprintf(file, "    clear_pool(&result_pool);\n");
    fprintf(file, "}\n");
}

void compile_monitor(char *name, nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    FILE *file;

    file = fopen(name, "wb");
    filter_log_msg(LOG_LEVEL_INFO, "Compiling specification to C code.\n");
    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting header code.\n");
    decompress_array_to_file(gensrc_compiler_headers_h_rdc, file);

    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting dictionaries.\n");
    export_dictionary("global_name", file, name_dict, EXPORT_DICT_USE_SIZE);
    export_dictionary("global_key", file, key_dict, EXPORT_DICT_USE_SIZE);
    // the value dictionary needs to be initialized to have room to grow
    // set the size to be defined by a #define
    export_dictionary("global_val", file, val_dict, "VALUE_DICTIONARY_SIZE");

    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting specification.\n");
    export_specification(file, spec, name_dict, key_dict, val_dict);

    // export global data structures
    fprintf(file, "pool input_pool, result_pool;\n");
    fprintf(file, "interval_node input_cache[NEW_INTERVALS_SIZE], result_cache[NEW_INTERVALS_SIZE];\n");
    fprintf(file, "map_value_node input_cache_map[NEW_INTERVALS_SIZE][%d], result_cache_map[NEW_INTERVALS_SIZE][%d];\n", key_dict->size, key_dict->size);

    // write the prototypes for initialization functions
    fprintf(file, "static void init_nfer(void);\n");
    fprintf(file, "static void wakeup(void);\n");

    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting source code.\n");
    decompress_array_to_file(gensrc_compiler_srccode_c_rdc, file);

    filter_log_msg(LOG_LEVEL_DEBUG, "Exporting initialization.\n");
    export_init(file, key_dict);

    fclose(file);
}


