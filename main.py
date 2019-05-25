import sys
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from timetable import Timetable
from commands.help import Help
from commands.load import Load
from commands.room import Room


help_command = Help()
room_command = Room()
_workbook = 5


def set_workbook(workbook):
    global _workbook
    _workbook = workbook


command = {
    "load": lambda x: set_workbook(Load.exec_command(x)),
    "room-table": lambda x: room_command.exec_comand(x),
    "help": lambda x: help_command.exec_command(x),
    "exit": lambda x: exit(0),
}


def input_mode():
    args = input("> ").split()
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


if __name__ == "__main__":
    main()

# workbook = load_workbook(filename='data/data.xlsx')
# sheet = workbook['zima-s']
#
# timetable = Timetable()
# # rooms = tools.get_with_not_null_column(tools.columnNameToIndex['sala'], sheet)
# # print(rooms[0][tools.columnNameToIndex['sala']].value)
# all_rooms = timetable.get_unique_value_from_column('sala', sheet)
# print(all_rooms)

#
# i=0
# for row in sheet.rows:
#     # print(row[columnNameToIndex['studia']].value)
#     for cell in row:
#         print(cell.value)
#     break

# first_column = sheet_ranges['D']
# print(*sheet_ranges)
# # # Print the contents
# for x in range(len(first_column)):
#     print(first_column[x].value)

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))
