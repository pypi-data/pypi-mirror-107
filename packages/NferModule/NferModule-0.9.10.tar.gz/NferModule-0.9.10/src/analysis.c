/*
 * analysis.c
 *
 *  Created on: Jun 2, 2017
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

#include "types.h"
#include "dict.h"
#include "nfer.h"
#include "log.h"
#include "analysis.h"
#include "memory.h"


void log_event_groups(nfer_specification *spec, dictionary *name_dict) {
    int i, j, new_group_num, *group_assignments, *group_counts;
    rule_id id;
    nfer_rule *rule;
    bool first;

    if (spec->subscription_size > 0) {
        filter_log_msg(LOG_LEVEL_DEBUG, "Subscription size %d\n", spec->subscription_size);

        // find event groups
        group_assignments = malloc(sizeof(int) * spec->subscription_size);
        clear_memory(group_assignments, sizeof(int) * spec->subscription_size);
        // can't have more groups than subscriptions
        group_counts = malloc(sizeof(int) * spec->subscription_size);
        clear_memory(group_counts, sizeof(int) * spec->subscription_size);
        new_group_num = 0;

        for (i = 0; i < spec->subscription_size; i++) {
            if (!group_assignments[i]) {
                new_group_num++;
                group_assignments[i] = new_group_num;
                group_counts[new_group_num - 1] = 1;
            }

            id = spec->subscriptions[LEFT_SUBSCRIPTIONS][i];
            while (id != MISSING_RULE_ID) {
                rule = &spec->rule_list.rules[id];
                id = rule->next[LEFT_SUBSCRIPTIONS];

                // mark right side
                if (!group_assignments[rule->right_label]) {
                    group_assignments[rule->right_label] = group_assignments[i];
                    group_counts[group_assignments[i] - 1]++;
                }
            }

            id = spec->subscriptions[RIGHT_SUBSCRIPTIONS][i];
            while (id != MISSING_RULE_ID) {
                rule = &spec->rule_list.rules[id];
                id = rule->next[RIGHT_SUBSCRIPTIONS];

                // mark left side
                if (!group_assignments[rule->left_label]) {
                    group_assignments[rule->left_label] = group_assignments[i];
                    group_counts[group_assignments[i] - 1]++;
                }
            }
        }

        for (j = 1; j <= new_group_num; j++) {
            if (group_counts[j - 1] > 1) {
                log_msg("Group %d:", j);
                first = true;

                for (i = 0; i < spec->subscription_size; i++) {
                    if (group_assignments[i] == j) {
                        if (!first) {
                            log_msg(",");
                        }
                        log_msg(" %s", get_word(name_dict, i));
                        first = false;
                    }
                }
                log_msg("\n");
            }
        }
        free(group_assignments);
        free(group_counts);
    }
}
