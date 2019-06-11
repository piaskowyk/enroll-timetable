from openpyxl import load_workbook

from commands.free_room import FreeRoom
from commands.help import Help
from commands.load import Load
from commands.room_table import RoomTable
from config_tools.configuration import Configuration
from spreadsheet_data.spreadsheet_data import *
from interface_tools.input_tools import *
from interface_tools.command_completion_tools import *
from pathlib import Path

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

configuration = Configuration(filepath="config.json")

_workbook = None
spreadsheet_data = None

# load sheet from default location (config.json)
sheet = Path(configuration.data['defaults_value']['path_to_sheet'])
if sheet.is_file():
    _workbook = load_workbook(configuration.data['defaults_value'][
                                  'path_to_sheet'])  # debugs
    spreadsheet_data = SpreadsheetData(configuration.data, _workbook)
    available_expressions["free"]['-r'] = spreadsheet_data.room_data.data
else:
    show_warning("First load data")

cmd_hist_file = open('commandHistory.txt', 'a+')
user_command_getter = UserCommandGetter(cmd_hist_file)

# set sheet data and configuration
def set_spreadsheet_data(data):
    global spreadsheet_data
    spreadsheet_data = data
    available_expressions["free"]['-r'] = spreadsheet_data.room_data.data


# program commands
command = {
    "load": lambda x: set_spreadsheet_data(Load.exec_command(x)),
    "room-table": lambda x: room_table_command.exec_command(spreadsheet_data,
                                                            x),
    "free": lambda x: free_room_command.exec_command(spreadsheet_data, x),
    "help": lambda x: help_command.exec_command(x),
    "exit": lambda x: exit(0),
}


def input_mode():
    # read user input
    args = user_command_getter.get_user_command()
    if spreadsheet_data is None and len(args) > 0 and args[0] != 'exit' and \
            args[0] != 'load':
        show_warning("First load data")
        return

    if len(args) < 1:
        print("unknown command")
    else:
        if args[0] in command:
            # execute inserted command
            command[args[0]](args)
        else:
            print("unknown command")
    return


def main():
    print("TIMETABLE-GENERATOR WIET 2019 - interactive mode")

    while True:
        input_mode()


if __name__ == "__main__":
    main()
