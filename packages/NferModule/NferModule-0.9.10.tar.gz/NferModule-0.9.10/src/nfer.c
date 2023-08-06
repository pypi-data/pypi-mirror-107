/*
 * nfer.c
 *
 *  Created on: Jan 19, 2017
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

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "nfer.h"
#include "dict.h"
#include "pool.h"
#include "stack.h"
#include "log.h"
#include "expression.h"
#include "memory.h"

#define PURGE_THRESHOLD 0.5

// We are using the hated global here, because there really is no reason why you would
// ever have different values in a process, and they are read only except from whatever
// user interface is being used
timestamp opt_window_size = NO_WINDOW;
bool opt_most_recent = false;
bool opt_full = false;

#ifndef NO_DYNAMIC_MEMORY
void initialize_specification(nfer_specification *spec, int size) {
    int i;
    spec->subscription_size = 0;
    for (i = 0; i < N_SUBSCRIPTION_LISTS; i++) {
        spec->subscriptions[i] = NULL;
    }
    resize_specification(spec, size);

    // allocate space for rules
    spec->rule_list.space = 0;
    spec->rule_list.size = 0;
    spec->rule_list.rules = (nfer_rule *) malloc(sizeof(nfer_rule) * INITIAL_RULE_LIST_LENGTH);
    if (spec->rule_list.rules != NULL) {
        spec->rule_list.space = INITIAL_RULE_LIST_LENGTH;
        clear_memory(spec->rule_list.rules, sizeof(nfer_rule) * INITIAL_RULE_LIST_LENGTH);
    }
}
void resize_specification(nfer_specification *spec, int size) {
    int side, old_size;
    rule_id *subscription_realloc;

    old_size = spec->subscription_size;
    // only do the work if we need to
    if (old_size < size) {
        for (side = 0; side < N_SUBSCRIPTION_LISTS; side++) {
            // this condition is safer, and lets us use the resize function from initialize
            if (spec->subscriptions[side] == NULL) {
                // allocate space for an array of pointers
                spec->subscriptions[side] = (rule_id *) malloc(sizeof(rule_id) * size);
            } else {
                subscription_realloc = (rule_id *) realloc(spec->subscriptions[side], sizeof(rule_id) * size);
                if (subscription_realloc) {
                    // only set the new value if it's not null
                    spec->subscriptions[side] = subscription_realloc;
                } else {
                    // otherwise make sure the size is still set to the old size and bail
                    // we have to reset back to the old size in case the realloc succeeded at least once
                    spec->subscription_size = old_size;
                    break;
                }
            }

            if (spec->subscriptions[side] != NULL) {
                // set the size var
                spec->subscription_size = size;
                // be careful to only set the new space
                set_memory(spec->subscriptions[side] + old_size, sizeof(rule_id) * (spec->subscription_size - old_size));
            }
        }
    }
}
void destroy_specification(nfer_specification *spec) {
    int i, side;
    nfer_rule *rule;
    map_iterator mit;
    map_key key;
    map_value value;

    spec->subscription_size = 0;
    // free subscriptions first
    for (side = 0; side < N_SUBSCRIPTION_LISTS; side++) {

        if (spec->subscriptions[side] != NULL) {
            free(spec->subscriptions[side]);
        }
        spec->subscriptions[side] = NULL;
    }

    // go through all the rules in the list and free the pools
    if (spec->rule_list.rules != NULL) {

        for (i = 0; i < spec->rule_list.size; i++) {
            rule = &spec->rule_list.rules[i];

            destroy_pool(&rule->new_intervals);
            destroy_pool(&rule->left_cache);
            destroy_pool(&rule->right_cache);
            destroy_pool(&rule->produced);
            // support exclusion
            rule->exclusion = false;

            // support the dsl data structures
            destroy_expression_input(&rule->where_expression);
            destroy_expression_input(&rule->begin_expression);
            destroy_expression_input(&rule->end_expression);
            get_map_iterator(&rule->map_expressions, &mit);
            while(has_next_map_key(&mit)) {
                key = next_map_key(&mit);
                map_get(&rule->map_expressions, key, &value);
                if (value.type == pointer_type) {
                    destroy_expression_input((expression_input **)(&value.pointer_value));
                }
            }
            destroy_map(&rule->map_expressions);
            destroy_stack(&rule->expression_stack);
        }
        free(spec->rule_list.rules);
        spec->rule_list.rules = NULL;
    }
    spec->rule_list.size = 0;
    spec->rule_list.space = 0;
}
#endif // no dynamic memory

// nfer operators
static bool before(timestamp UNUSED(s1), timestamp e1, timestamp s2, timestamp UNUSED(e2)) {
    return e1 < s2;
}
static bool meet(timestamp UNUSED(s1), timestamp e1, timestamp s2, timestamp UNUSED(e2)) {
    return e1 == s2;
}
static bool during(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 >= s2 && e1 <= e2;
}
static bool coincide(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 == s2 && e1 == e2;
}
static bool start(timestamp s1, timestamp UNUSED(e1), timestamp s2, timestamp UNUSED(e2)) {
    return s1 == s2;
}
static bool finish(timestamp UNUSED(s1), timestamp e1, timestamp UNUSED(s2), timestamp e2) {
    return e1 == e2;
}
static bool overlap(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s1 < e2 && s2 < e1;
} // also used for slice

// exclusion operators
static bool after(timestamp s1, timestamp UNUSED(e1), timestamp UNUSED(s2), timestamp e2)  {
    return s1 > e2;
}
static bool follow(timestamp s1, timestamp UNUSED(e1), timestamp UNUSED(s2), timestamp e2) {
    return s1 == e2;
}
static bool contain(timestamp s1, timestamp e1, timestamp s2, timestamp e2) {
    return s2 >= s1 && e2 < e1;
}

// start and end time functions
static timestamp start_end_1(timestamp t1, timestamp UNUSED(t2)) {
    return t1;
}
static timestamp start_end_2(timestamp UNUSED(t1), timestamp t2) {
    return t2;
}
static timestamp start_end_min(timestamp t1, timestamp t2) {
    if (t1 < t2) {
        return t1;
    } else {
        return t2;
    }
}
static timestamp start_end_max(timestamp t1, timestamp t2) {
    if (t1 > t2) {
        return t1;
    } else {
        return t2;
    }
}
/**********
 * Nfer operators as predefined, including negations
 **********/
nfer_operator operators[] = {
        { "also", NULL, start_end_1, start_end_1, false }, // default to using ends from the left-hand interval, since also is used for atomic rules
        { "before", before, start_end_1, start_end_2, false },
        { "meet", meet, start_end_1, start_end_2, false },
        { "during", during, start_end_2, start_end_2, false },
        { "coincide", coincide, start_end_1, start_end_2, false },
        { "start", start, start_end_1, start_end_max, false },
        { "finish", finish, start_end_min, start_end_2, false },
        { "overlap", overlap, start_end_min, start_end_max, false },
        { "slice", overlap, start_end_max, start_end_min, false },
        // negations
        { "after", after, start_end_1, start_end_1, true },
        { "follow", follow, start_end_1, start_end_1, true },
        { "contain", contain, start_end_1, start_end_1, true }
};

nfer_rule * add_rule_to_specification(nfer_specification *spec,
        label result_label_index, label left_label_index, operator_code op_code, label right_label_index, phi_function *phi) {
    nfer_rule_list *rule_list;
    nfer_rule *rule = NULL;
    rule_id id = MISSING_RULE_ID;
    label max_label_index;

    // get a reference to the rule list
    rule_list = &spec->rule_list;
#ifndef NO_DYNAMIC_MEMORY
    // check to make sure there is room...
    if (rule_list->space <= rule_list->size) {
        // there isn't enough room.  Allocate more.
        if (rule_list->rules != NULL) {
            rule_list->space = rule_list->space * 2;
            rule_list->rules = realloc(rule_list->rules, sizeof(nfer_rule) * rule_list->space);
            // clear anything above size to the end
            clear_memory(rule_list->rules + rule_list->size, sizeof(nfer_rule) * (rule_list->space - rule_list->size));
        }
    }
#endif
    if (rule_list->rules != NULL && rule_list->size < rule_list->space) {
        id = rule_list->size;
        rule = &rule_list->rules[id];

        // initialize the pools
        initialize_pool(&rule->new_intervals);
        initialize_pool(&rule->left_cache);
        initialize_pool(&rule->right_cache);
        initialize_pool(&rule->produced);

        // set the operator
        if (op_code > 0 && op_code < N_OPERATORS) {
            rule->op_code = op_code;
            rule->exclusion = operators[op_code].exclusion;
        } else {
            // default to also
            rule->op_code = ALSO_OPERATOR;
            rule->exclusion = false;
        }

        // set phi function
        rule->phi = phi;

        // set all the fields for DSL support to empty by default
        // default to not being hidden
        rule->hidden = false;
        rule->where_expression = NULL;
        rule->begin_expression = NULL;
        rule->end_expression = NULL;
        rule->map_expressions = EMPTY_MAP;
        initialize_stack(&rule->expression_stack);

        // then set the common fields
        rule->left_label = left_label_index;
        rule->right_label = right_label_index;
        rule->result_label = result_label_index;

#ifndef NO_DYNAMIC_MEMORY
        // ideally the caller would do this first, but for safety, make sure the subscription
        // arrays are big enough
        max_label_index = right_label_index;
        if (left_label_index > max_label_index) {
            max_label_index = left_label_index;
        }
        if (result_label_index > max_label_index) {
            max_label_index = result_label_index;
        }
        filter_log_msg(LOG_LEVEL_DEBUG, "Resizing specification to %d\n", max_label_index);
        resize_specification(spec, max_label_index + 1);
#endif

        if (spec->subscription_size > left_label_index) {
            // add to the subscription index linked lists
            rule->next[LEFT_SUBSCRIPTIONS] = spec->subscriptions[LEFT_SUBSCRIPTIONS][left_label_index];
            spec->subscriptions[LEFT_SUBSCRIPTIONS][left_label_index] = id;
        }
        if (spec->subscription_size > right_label_index) {
            // this test is needed to support atomic rules
            if (right_label_index != WORD_NOT_FOUND) {
                rule->next[RIGHT_SUBSCRIPTIONS] = spec->subscriptions[RIGHT_SUBSCRIPTIONS][right_label_index];
                spec->subscriptions[RIGHT_SUBSCRIPTIONS][right_label_index] = id;
            }
        }

        // increment the size
        rule_list->size++;
    }

    return rule;
}

/**
 * Checks if a label has been subscribed to by a specification
 */
bool is_subscribed(nfer_specification *spec, label name) {
    if (spec->subscription_size > name) {
        if (spec->subscriptions[LEFT_SUBSCRIPTIONS][name] != MISSING_RULE_ID ||
            spec->subscriptions[RIGHT_SUBSCRIPTIONS][name] != MISSING_RULE_ID) {
            return true;
        }
    }
    return false;
}

/**
 * Checks if a label may be published by a specification
 */
bool does_publish(nfer_specification *spec, label name) {
    int i;
    nfer_rule *rule;

    for (i = 0; i < spec->rule_list.size; i++) {
        rule = &spec->rule_list.rules[i];
        if (rule->result_label == name && !rule->hidden) {
            return true;
        }
    }
    return false;
}


static void select_minimal(pool *potentials, pool *prior) {
    interval *new, *old;
    pool_iterator new_pit, old_pit;
    bool removed;

    if (potentials->size > 0) {
        // perform a minimality check
        get_pool_iterator(potentials, &new_pit);
        while (has_next_interval(&new_pit)) {
            new = next_interval(&new_pit);
            removed = false;

            // first check against the other potentials
            get_pool_iterator(potentials, &old_pit);
            while (has_next_interval(&old_pit)) {
                old = next_interval(&old_pit);
                if (old != new) {
                    if (old->start >= new->start && old->end <= new->end) {
                        // remove the candidate
                        remove_from_pool(&new_pit);
                        removed = true;
                        break;
                    }
                }
            }

            // then check against the prior intervals
            // skip it if we already removed
            if (!removed) {
                get_pool_iterator(prior, &old_pit);
                while (has_next_interval(&old_pit)) {
                    old = next_interval(&old_pit);
                    if (old->start >= new->start && old->end <= new->end) {
                        // remove the candidate
                        remove_from_pool(&new_pit);
                        break;
                    }
                }
            }
        }
    } // if potentials is non-empty
}

static bool interval_match(nfer_rule *rule, interval *lhs, interval *rhs) {
    nfer_operator *op;
    bool op_succeeded, phi_succeeded;
    typed_value where_succeeded;

    // we should be able to safely assume that there is an op_code
    op = &operators[rule->op_code];
    op_succeeded = true;
    // if there is a test function, use it, otherwise default to true
    if (op->test != NULL) {
        // test the operator to see if it is met
        op_succeeded = op->test(lhs->start, lhs->end, rhs->start, rhs->end);
    }
    // if there's a phi function, test it, otherwise default to success
    phi_succeeded = true;
    if (rule->phi != NULL && rule->phi->test != NULL) {
        phi_succeeded = rule->phi->test(lhs->start, lhs->end, &lhs->map, rhs->start, rhs->end, &rhs->map);
    }
    // if there is a where clause from the DSL, use it, otherwise default to success
    where_succeeded.type = boolean_type;
    where_succeeded.boolean_value = true;

    if (rule->where_expression != NULL) {
        evaluate_expression(rule->where_expression, &where_succeeded, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
    }

    // the op, phi, and where clause must all succeed to match an interval
    // We're just using the boolean value of where_succeeded without type checking at runtime
    // we assume that static type checking worked.
    return op_succeeded && phi_succeeded && where_succeeded.boolean_value;
}

static void set_end_times(nfer_rule *rule, interval *lhs, interval *rhs, interval *result) {
    typed_value time_result;
    nfer_operator *op;
    op = &operators[rule->op_code];

    // begin and end expressions from the DSL override operator begin and end times
    if (rule->begin_expression != NULL) {
        evaluate_expression(rule->begin_expression, &time_result, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        if (time_result.type == real_type) {
            result->start = (timestamp)time_result.real_value;
        } else {
            // this is relying on static type checking from the DSL to work, otherwise we could get some randomness
            result->start = time_result.integer_value;
        }
    } else {
        // semantic analysis should guarantee that this is not null
        result->start = op->start_time(lhs->start, rhs->start);
    }
    if (rule->end_expression != NULL) {
        evaluate_expression(rule->end_expression, &time_result, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        if (time_result.type == real_type) {
            result->end = (timestamp)time_result.real_value;
        } else {
            // this is relying on static type checking from the DSL to work, otherwise we could get some randomness
            result->end = time_result.integer_value;
        }
    } else {
        // semantic analysis should guarantee that this is not null
        result->end = op->end_time(lhs->end, rhs->end);
    }
}

static void set_map(nfer_rule *rule, interval *lhs, interval *rhs, data_map *result) {
    map_iterator mit;
    map_key key_to_set;
    map_value map_expression, value_to_set;

    // if there's a phi function, use it first
    if (rule->phi != NULL && rule->phi->result != NULL) {
        // if the phi function exists
        // use it to set the map and then add
        rule->phi->result(result, lhs->start, lhs->end, &lhs->map, rhs->start, rhs->end, &rhs->map);
    }

    // if there are map expressions from the DSL, use them
    get_map_iterator(&rule->map_expressions, &mit);
    while (has_next_map_key(&mit)) {
        key_to_set = next_map_key(&mit);
        map_get(&rule->map_expressions, key_to_set, &map_expression);

        // it should (must) be a pointer to an expression_input
        evaluate_expression((expression_input *)map_expression.pointer_value, &value_to_set, &rule->expression_stack,
                lhs->start, lhs->end, &lhs->map,
                rhs->start, rhs->end, &rhs->map);
        // set the key to whatever was returned
        map_set(result, key_to_set, &value_to_set);
    }
}

static void discard_older_events(pool *cache, timestamp cutoff) {
    pool_iterator pit;
    interval *i;

    get_pool_iterator(cache, &pit);
    while (has_next_interval(&pit)) {
        i = next_interval(&pit);
        if (i->end < cutoff) {
            remove_from_pool(&pit);
        }
    }
    // above some threshold, purge the pool to free up space
    // the threshold is if the number of removed items is at least some percent of the total size
    // purge_pool is O(n), so this isn't too expensive.  Maybe try decreasing the threshold.
    if ((float)cache->removed / (float)cache->size > PURGE_THRESHOLD) {
        filter_log_msg(LOG_LEVEL_INFO, "Purging pool %x due to removed reaching threshold %f\n", cache, PURGE_THRESHOLD);
        purge_pool(cache);
    }
}

void add_interval_to_specification(nfer_specification *spec, interval *add, pool *out) {
    rule_id rule_index;
    nfer_rule *rule;
    interval *rhs, *lhs, *new, *accepted;
    word_id lhs_label, rhs_label;
    pool_iterator left_pit, right_pit, new_pit;
    bool exclude;

    // optimization related
    timestamp window_cutoff = add->end - opt_window_size;

    // it is possible to receive events for which we are not sized
    // just ignore them, as they aren't handled by this spec
    if (add->name >= spec->subscription_size) {
        filter_log_msg(LOG_LEVEL_DEBUG, "Ignoring %d interval because it is outside the range of the specification\n", add->name);
        return;
    }

    if (spec->subscriptions[LEFT_SUBSCRIPTIONS] != NULL) {
        lhs_label = add->name;
        // The index has to be within bounds
        rule_index = spec->subscriptions[LEFT_SUBSCRIPTIONS][lhs_label];
        while (rule_index != MISSING_RULE_ID) {
            rule = &spec->rule_list.rules[rule_index];
            // advance the id to the next in the "linked" list
            rule_index = rule->next[LEFT_SUBSCRIPTIONS];

            // clear the potential new interval pool
            clear_pool(&rule->new_intervals);

            // handle exclusions first
            if (rule->exclusion) {
                exclude = false;
                // go through the rhs cache to see if something has occurred to negate this interval
                get_pool_iterator(&rule->right_cache, &right_pit);
                while (has_next_interval(&right_pit)) {
                    rhs = next_interval(&right_pit);

                    // if a window is used, remove the interval if it is too old
                    if (opt_window_size != NO_WINDOW) {
                        if (rhs->end < window_cutoff) {
                            remove_from_pool(&right_pit);
                            continue;
                        }
                    }

                    // rhs must come before add (this is part of the semantics of negation)
                    if (rhs->end < add->end) {
                        // check the exclusion conditions just like any other operator
                        if (interval_match(rule, add, rhs)) {
                            // if the conditions hold, exclude the match
                            exclude = true;
                            break;
                        }
                    }
                }
                // the interval is not negated
                if (!exclude) {
                    // get a new interval from the new_intervals pool
                    new = allocate_interval(&rule->new_intervals);

                    // set the end times using the helper function
                    // use add as the rhs as semantic analysis should guarantee it doesn't matter
                    set_end_times(rule, add, add, new);
                    new->name = rule->result_label;

                    // again, add is rhs and it doesn't matter
                    set_map(rule, add, add, &new->map);
                }

            } else { // not an exclusion

                // if this isn't an atomic rule
                if (rule->right_label != WORD_NOT_FOUND) {
                    // go through the rhs cache for matches
                    get_pool_iterator(&rule->right_cache, &right_pit);
                    while (has_next_interval(&right_pit)) {
                        rhs = next_interval(&right_pit);

                        // if a window is used, remove the interval if it is too old
                        if (opt_window_size != NO_WINDOW) {
                            if (rhs->end < window_cutoff) {
                                remove_from_pool(&right_pit);
                                continue;
                            }
                        }

                        // the op, phi, and where clause must all succeed to match an interval
                        if (interval_match(rule, add, rhs)) {
                            // get a new interval from the new_intervals pool
                            new = allocate_interval(&rule->new_intervals);

                            // set the end times using the helper function
                            set_end_times(rule, add, rhs, new);
                            new->name = rule->result_label;

                            set_map(rule, add, rhs, &new->map);
                        }
                    } // for right_cache

                } else {
                    // this is an atomic rule, so just test
                    // set rhs to add just to it doesn't segfault -- the values shouldn't matter
                    if (interval_match(rule, add, add)) {
                        // get a new interval from the new_intervals pool
                        new = allocate_interval(&rule->new_intervals);

                        // set the end times using the helper function
                        // again use add as the rhs, again it shouldn't matter
                        set_end_times(rule, add, add, new);

                        new->name = rule->result_label;

                        // again, add is rhs and it doesn't matter
                        set_map(rule, add, add, &new->map);
                    }
                }
            }

            // skip this work if not testing for minimality
            if (!opt_full) {
                // before testing minimality, if a window is used, remove anything from the produced pool that is too old
                if (opt_window_size != NO_WINDOW) {
                    discard_older_events(&rule->produced, window_cutoff);
                }

                // now check for minimality and remove anything that isn't
                select_minimal(&rule->new_intervals, &rule->produced);
            }
            // finally add anything left to the produced pool, and to the output if the rule isn't hidden
            // recurse on the interval being added
            get_pool_iterator(&rule->new_intervals, &new_pit);
            while(has_next_interval(&new_pit)) {
                accepted = next_interval(&new_pit);
                /* set the hidden flag */
                accepted->hidden = rule->hidden;

                // skip adding to the produced pool if not using minimality
                if (!opt_full) {
                    add_interval(&rule->produced, accepted);
                }
                add_interval(out, accepted);
            }

            // if using the most recent optimization, clear the cache before adding
            if (opt_most_recent) {
                clear_pool(&rule->left_cache);
            }
            // add to the left hand cache (we have to be careful about this later)
            add_interval(&rule->left_cache, add);

        } // while rule != null
    } // left_subscriptions != NULL

    if (spec->subscriptions[RIGHT_SUBSCRIPTIONS] != NULL) {
        rhs_label = add->name;
        // The index has to be within bounds
        rule_index = spec->subscriptions[RIGHT_SUBSCRIPTIONS][rhs_label];
        while (rule_index != MISSING_RULE_ID) {
            rule = &spec->rule_list.rules[rule_index];
            // advance the id to the next in the "linked" list
            rule_index = rule->next[RIGHT_SUBSCRIPTIONS];

            // skip to the next one if the rule is a negation
            if (!rule->exclusion) {

                // clear the potential new interval pool
                clear_pool(&rule->new_intervals);

                // go through the lhs cache for matches
                get_pool_iterator(&rule->left_cache, &left_pit);
                while (has_next_interval(&left_pit)) {
                    lhs = next_interval(&left_pit);

                    // if a window is used, remove the interval if it is too old
                    if (opt_window_size != NO_WINDOW) {
                        if (lhs->end < window_cutoff) {
                            remove_from_pool(&left_pit);
                            continue;
                        }
                    }

                    // BE CAREFUL!  We already added this interval to the left cache, but
                    // we don't want to match against the _same_ interval.
                    if (equal_intervals(lhs, add)) {
                        // lhs is the exact same interval as add.
                        // Skip!
                        continue;
                    }

                    // the op, phi, and where clause must all succeed to match an interval
                    if (interval_match(rule, lhs, add)) {
                        // get a new interval from the new_intervals pool
                        new = allocate_interval(&rule->new_intervals);

                        // set the end times using the helper function
                        set_end_times(rule, lhs, add, new);
                        new->name = rule->result_label;

                        set_map(rule, lhs, add, &new->map);
                    }
                } // for left_cache

                // skip this work if not testing for minimality
                if (!opt_full) {
                    // before testing minimality, if a window is used, remove anything from the produced pool that is too old
                    if (opt_window_size != NO_WINDOW) {
                        discard_older_events(&rule->produced, window_cutoff);
                    }

                    // now check for minimality and remove anything that isn't
                    select_minimal(&rule->new_intervals, &rule->produced);
                }

                // finally add anything left to the produced pool, and to the output if the rule isn't hidden
                // recurse on the interval being added
                get_pool_iterator(&rule->new_intervals, &new_pit);
                while(has_next_interval(&new_pit)) {
                    accepted = next_interval(&new_pit);
                    /* set the hidden flag */
                    accepted->hidden = rule->hidden;

                    // skip adding to the produced pool if not using minimality
                    if (!opt_full) {
                        add_interval(&rule->produced, accepted);
                    }
                    add_interval(out, accepted);
                }
            }

            // if using the most recent optimization, clear the cache before adding
            if (opt_most_recent) {
                clear_pool(&rule->right_cache);
            }
            // add to the right hand cache
            add_interval(&rule->right_cache, add);

        } // while rule != null
    } // right_subscriptions != NULL

}

/**
 * For embedded goodness, we avoid recursion.
 */
void run_nfer(nfer_specification *spec, pool *input_pool, pool *output_pool) {
    int out_pool_index, cycle;
    interval *intv;
    pool_iterator pit;
    pool internal_pool[2], *in, *out;
    bool converged = false;

    // initially, point at the input pool
    in = input_pool;
    out_pool_index = 0;
    cycle = 0;

    filter_log_msg(LOG_LEVEL_DEBUG, "Running nfer...\n");

    while (!converged) {
        cycle++;
        filter_log_msg(LOG_LEVEL_DEBUG, "Starting cycle %d\n", cycle);

        // set up the output pool
        out = &internal_pool[out_pool_index % 2];
        out_pool_index++;
        initialize_pool(out);

        // now run the nfer spec on the intervals in the pool
        get_pool_iterator(in, &pit);
        while (has_next_interval(&pit)) {
            intv = next_interval(&pit);
            if (should_log(LOG_LEVEL_DEBUG)) {
                log_msg("Adding interval to spec (%d,%" PRIu64 ",%" PRIu64 ",", intv->name, intv->start, intv->end);
                log_map(&intv->map);
                log_msg(")\n");
            }
            // test the specification on each interval in the pool
            add_interval_to_specification(spec, intv, out);
        }

        // make sure not to mess up the input
        if (in != input_pool) {
            destroy_pool(in);
        }
        // swap in for out
        in = out;

        if (out->size > 0) {
            // add the resulting intervals to the output pool, just appending for now
            // make sure to exclude the hidden intervals
            copy_pool(output_pool, out, COPY_POOL_APPEND, COPY_POOL_EXCLUDE_HIDDEN);
        } else {
            // nothing new, we converged
            converged = true;
        }
    }

    // final teardown
    if (cycle > 0) {
        destroy_pool(out);
    }
    // sort the result
    if (output_pool->size > 0) {
        sort_pool(output_pool);
    }
}



static void write_rule(nfer_rule *rule, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, int log_to) {
    map_iterator mit;
    map_key key;
    map_value value;
    bool first;
    nfer_operator *op;

    op = &operators[rule->op_code];

    if (rule->exclusion) {
        // there isn't exclusion support in the dsl right now, so this is all we need
        write_msg(log_to, "%s :- %s unless %s %s",
                get_word(name_dict, rule->result_label),
                get_word(name_dict, rule->left_label),
                op->name,
                get_word(name_dict, rule->right_label));
    } else {
        // need to support both the C API and the DSL
        write_msg(log_to, "%s :- %s %s %s",
                get_word(name_dict, rule->result_label),
                get_word(name_dict, rule->left_label),
                op->name,
                get_word(name_dict, rule->right_label));
    }
    if (rule->phi) {
        write_msg(log_to, " phi %s ", rule->phi->name);
    }
    if (rule->where_expression) {
        write_msg(log_to, " where ");
        write_expression(rule->where_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    if (rule->begin_expression) {
        write_msg(log_to, " begin ");
        write_expression(rule->begin_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    if (rule->end_expression) {
        write_msg(log_to, " end ");
        write_expression(rule->end_expression, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
    }
    get_map_iterator(&rule->map_expressions, &mit);
    if (has_next_map_key(&mit)) {
        write_msg(log_to, " map { ");
        first = true;
        while(has_next_map_key(&mit)) {
            if (first) {
                first = false;
            } else {
                log_msg(", ");
            }
            key = next_map_key(&mit);
            map_get(&rule->map_expressions, key, &value);
            write_msg(log_to, "%s -> ", get_word(key_dict, key));
            write_expression(value.pointer_value, key_dict, val_dict, get_word(name_dict, rule->left_label), get_word(name_dict, rule->right_label), log_to);
        }
        write_msg(log_to, " }");
    }
}

void log_specification(nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    int i;
    filter_log_msg(LOG_LEVEL_DEBUG, "Specification(%d,%d,%p,%d,%p,%p)\n",
            spec->rule_list.space,
            spec->rule_list.size,
            spec->rule_list.rules,
            spec->subscription_size,
            spec->subscriptions[LEFT_SUBSCRIPTIONS],
            spec->subscriptions[RIGHT_SUBSCRIPTIONS]);
    for (i = 0; i < spec->rule_list.size; i++) {
        write_rule(&spec->rule_list.rules[i], name_dict, key_dict, val_dict, WRITE_LOGGING);
        log_msg("\n");
    }
}

void output_specification(nfer_specification *spec, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict) {
    int i;
    for (i = 0; i < spec->rule_list.size; i++) {
        write_rule(&spec->rule_list.rules[i], name_dict, key_dict, val_dict, WRITE_OUTPUT);
        write_msg(WRITE_OUTPUT, "\n");
    }
}

