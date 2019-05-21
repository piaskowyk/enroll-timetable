import sys
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from timetable import Timetable

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))

def main():
    print("TIMETABLE-GENERATOR")

    workbook = load_workbook(filename='data/data.xlsx')
    sheet = workbook['zima-s']

    timetable = Timetable()
    # rooms = tools.get_with_not_null_column(tools.columnNameToIndex['sala'], sheet)
    # print(rooms[0][tools.columnNameToIndex['sala']].value)
    all_rooms = timetable.get_unique_value_from_column('sala', sheet)
    print(all_rooms)


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


if __name__ == "__main__":
    main()

