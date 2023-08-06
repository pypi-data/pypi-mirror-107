/*
 * linux.c
 *
 *  Created on: Jun 8, 2018
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

/*********
 * This file isn't meant to be compiled with the main application.
 * It is here to be included with "compiled" monitors where the target OS is Linux
 *********/

#if TARGET==linux
// for Linux, it should be main
int main(void) {
    int line_number;
    bool read_success;
    char line[MAX_LINE_LENGTH];

    init_nfer();

    line_number = 0;

    while (fgets(line, MAX_LINE_LENGTH, stdin)) {
        line_number++;
        read_success = read_event_from_csv(&input_pool, line, line_number, &global_name_dict, &global_key_dict, &global_val_dict, true);

        if (read_success) {
            wakeup();
            clear_pool(&input_pool);
        }
    }

    return 0;
}
#endif
