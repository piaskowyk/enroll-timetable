from interface_tools.getch import _Getch
from interface_tools.output_tools import *
from interface_tools.command_completion_tools import *
import sys


class UserCommandGetter:
    getch = None
    user_command = None
    cur_user_command = None
    cmd_hist_file = None
    cursor_pos = None
    cur_cursor_pos = None

    def __init__(self, cmd_hist_file):
        self.getch = _Getch()
        self.user_command = ''
        self.cur_user_command = ''
        self.cmd_hist_file = cmd_hist_file
        self.cursor_pos = 0

    def get_user_command(self):
        self.user_command = ''
        self.cur_user_command = ''
        self.cmd_hist_file.seek(0)
        cmd_hist = self.cmd_hist_file.readlines()
        hist_cmd_id = 0
        ret_val = self.get_next_char()
        self.cursor_pos = 0
        self.cur_cursor_pos = 0
        while ret_val != 0:
            if ret_val == 1:
                self.cursor_pos += 1
            if ret_val == 3:
                if hist_cmd_id < len(cmd_hist):
                    hist_cmd_id += 1
                    self.user_command = cmd_hist[-hist_cmd_id][0:-1]
                    self.cursor_pos = len(self.user_command)
            if ret_val == 4:
                if hist_cmd_id > 0:
                    hist_cmd_id -= 1
                    if hist_cmd_id == 0:
                        self.user_command = self.cur_user_command
                        self.cursor_pos = self.cur_cursor_pos
                    else:
                        self.user_command = cmd_hist[-hist_cmd_id][0:-1]
                        self.cursor_pos = len(self.user_command)
            if ret_val == 5:
                command_completion = complete_command(
                    self.user_command[:self.cursor_pos])
                self.user_command = self.user_command[:self.cursor_pos] + \
                                    command_completion + self.user_command[
                                                         self.cursor_pos:]
                self.cursor_pos += len(command_completion)
            if ret_val == 6:
                if self.cursor_pos < len(self.user_command):
                    self.cursor_pos += 1
            if ret_val == 7:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            if hist_cmd_id == 0:
                self.cur_user_command = self.user_command
                self.cur_cursor_pos = self.cursor_pos
            ret_val = self.get_next_char()
        print()
        self.cmd_hist_file.write(self.user_command + '\n')
        self.cmd_hist_file.flush()
        return self.user_command.split()

    def get_next_char(self):
        print('\r', ' ' * 80, '\r', end='')
        show_prompt()
        print(self.user_command, end='')
        print((len(self.user_command) - self.cursor_pos) * '\b', end='')
        sys.stdout.flush()
        cur_char = self.getch.__call__()
        if cur_char == chr(13):
            return 0
        if cur_char == chr(127):
            if self.cursor_pos > 0:
                self.user_command = self.user_command[:self.cursor_pos - 1] + \
                                    self.user_command[self.cursor_pos:]
                self.cursor_pos -= 1
            return 2
        if cur_char == chr(126):
            if self.cursor_pos < len(self.user_command):
                self.user_command = self.user_command[:self.cursor_pos] + \
                                    self.user_command[self.cursor_pos + 1:]
            return 2
        if cur_char == chr(27):
            extra1 = self.getch.__call__()
            extra2 = self.getch.__call__()
            if extra1 == '[' and extra2 == 'A':
                return 3
            if extra1 == '[' and extra2 == 'B':
                return 4
            if extra1 == '[' and extra2 == 'C':
                return 6
            if extra1 == '[' and extra2 == 'D':
                return 7
            return -1
        if cur_char == '\t':
            return 5
        if cur_char == chr(3):
            self.user_command = 'exit'
            return 0
        self.user_command = self.user_command[:self.cursor_pos] + \
                            cur_char + self.user_command[self.cursor_pos:]
        return 1
