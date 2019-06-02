import sys
import time

from openpyxl import load_workbook

from commands.free_room import FreeRoom
from commands.help import Help
from commands.load import Load
from commands.room_table import RoomTable
from config_tools.configuration import Configuration
from spreadsheet_data.spreadsheet_data import *

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

sys.stdout.write(CURSOR_UP_ONE)
sys.stdout.write(ERASE_LINE)


def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


help_command = Help()
room_table_command = RoomTable()
free_room_command = FreeRoom()

#_workbook = None
_workbook = load_workbook(filename='data/data.xlsx')#debugs
configuration = Configuration(filepath="config.json")
#_spreadsheet_data = None
spreadsheet_data = SpreadsheetData(configuration.data, _workbook)


def set_spreadsheet_data(data):
    global _spreadsheet_data
    _spreadsheet_data = data


command = {
    "load": lambda x: set_spreadsheet_data(Load.exec_command(x)),
    "room-table": lambda x: room_table_command.exec_command(spreadsheet_data, x),
    "free-room-in-time": lambda x: free_room_command.find_free_rooms_in_time(spreadsheet_data, x),
    "free-time-in-room": lambda x: free_room_command.find_free_times_in_room(spreadsheet_data, x),
    "help": lambda x: help_command.exec_command(x),
    "exit": lambda x: exit(0),
}


def input_mode():
    # args = input("> ").split() #debug
    # args = ["room-table", "./data/tmp.pdf"] #debug
    # args = ["free-room-in-time", "-d", "Pn", "-h", "12:50"] #debug
    args = ["free-time-in-room", "-r", "D17:1.38"] #debug
    if len(args) < 1:
        print("unknown command")
    else:
        if args[0] in command:
            command[args[0]](args)
        else:
            print("unknown command")
    return


def main():
    print("TIMETABLE-GENERATOR WIET 2019 - interactive mode")

    while True:
        input_mode()
        return #debug


if __name__ == "__main__":
    main()
