import sys
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from timetable import Timetable
from commands.help import Help
from commands.load import Load
from commands.room import Room
from config_tools.configuration import Configuration
from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter
from spreadsheet_data.building_data import *
from spreadsheet_data.room_data import *
from spreadsheet_data.department_data import *
from spreadsheet_data.trainer_data import *


help_command = Help()
room_command = Room()
_workbook = load_workbook(filename='data/data.xlsx')#debugs
configuration = Configuration(filepath="config.json")


def set_workbook(workbook):
    global _workbook
    _workbook = workbook


command = {
    "load": lambda x: set_workbook(Load.exec_command(x)),
    "room-table": lambda x: room_command.exec_comand(x, _workbook),
    "help": lambda x: help_command.exec_command(x),
    "exit": lambda x: exit(0),
}


def input_mode():
    args = input("> ").split()#debug
    # args = ["room-table", "a"]#debug
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
    building_data = BuildingData()
    room_data = RoomData(configuration.data, _workbook, building_data)
    department_data = DepartmentData()
    trainer_data = TrainerData(configuration.data, _workbook, department_data)


    while True:#debug
        input_mode()


if __name__ == "__main__":
    main()

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))
