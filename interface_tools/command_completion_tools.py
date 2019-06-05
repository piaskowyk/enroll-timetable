from utils.timetabletools import TimetableTools
from spreadsheet_data.room_data import *

available_expressions = {
    "load": {},
    "room-table": {},
    "free-room-in-time": {
        '-d': TimetableTools.days_of_week_label,
        '-h': TimetableTools.time_blocks,
        '-c': {},
        '-t': room_types
    },
    "free-time-in-room": {},
    "help": {},
    "exit": {}
}


def search_completion_from_dict(current_expression, expr_dict):
    cmd_len = len(current_expression)
    found_key = None
    more_keys_found = False
    for key, value in expr_dict.items():
        if key[0: cmd_len] == current_expression:
            if found_key is None:
                found_key = key
            else:
                if not more_keys_found:
                    print('\n', found_key, end='')
                    more_keys_found = True
                print('    ', key, end='')
                found_key = longestSubstringFinder(found_key, key)
    if more_keys_found:
        print()
    if found_key is None:
        return ''
    else:
        return_str = found_key[cmd_len:]
        if not more_keys_found:
            return_str += ' '
        return return_str


def complete_command(current_command):
    cmd_split_len = len(current_command.split())
    if cmd_split_len == 0 or (cmd_split_len == 1 and
                              current_command.split()[0] not in
                              available_expressions):
        return search_completion_from_dict(current_command,
                                           available_expressions)
    rest_expr = current_command.split()[1:]
    command = current_command.split()[0]
    if command not in available_expressions:
        return ''
    if len(rest_expr) == 0 and current_command[-1] != ' ':
        return ' '
    expected_flag = True
    cur_flag = None
    while len(rest_expr) > 0:
        space_at_end = True
        if len(rest_expr) == 1:
            if current_command[-1] != ' ':
                space_at_end = False
        if expected_flag:
            cur_flag = rest_expr[0]
            if cur_flag in available_expressions[command] and space_at_end:
                expected_flag = False
        else:
            cur_key = rest_expr[0]
            if (cur_key in available_expressions[command][
                cur_flag] or len(available_expressions[command][
                                     cur_flag]) == 0) and space_at_end:
                expected_flag = True
                cur_flag = None
        if len(rest_expr) == 1:
            break
        else:
            rest_expr = rest_expr[1:]
    if expected_flag:
        if len(rest_expr) == 0:
            return search_completion_from_dict('',
                                               available_expressions[command])
        else:
            cur_expr = rest_expr[0]
            if cur_expr[0] != '-':
                cur_expr = ''
            return search_completion_from_dict(cur_expr,
                                               available_expressions[command])
    else:
        cur_expr = rest_expr[0]
        if len(available_expressions[command][cur_flag]) == 0:
            if cur_expr in available_expressions[command]:
                return ''
            else:
                return ' '
        else:
            if cur_expr in available_expressions[command]:
                cur_expr = ''
            return search_completion_from_dict(cur_expr,
                                               available_expressions[command][
                                                   cur_flag])


def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        if i < len2:
            if string1[i] == string2[i]:
                answer += string1[i]
            else:
                break
        else:
            break
    return answer
