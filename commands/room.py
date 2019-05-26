from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from timetable import Timetable


class Room:

    def __init__(self):
        self.tools = Timetable()

    def exec_comand(self, args, workbook):
        print("start")
        sheet = workbook['zima-s']
        timetable = Timetable()
        all_rooms = sorted(timetable.get_unique_value_from_column('sala', sheet.rows))
        # print(all_rooms)
        exist_room = self.tools.get_with_not_null_column('sala', sheet.rows)
        exist_room_day = self.tools.get_with_not_null_column('dzien', exist_room)
        exist_room_day_time = self.tools.get_with_not_null_column('dzien', exist_room_day)
        for room in all_rooms:
            print("Room ", room)
            room_data = self.tools.get_with_column_equals('sala', room, exist_room_day_time)
            for day in self.tools.days_of_week[0:5]:
                print(day)
            print("----------------------------")
        # for item in exist_room_date:
        #     print(item[self.tools.columnNameToIndex['sala']].value)

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
