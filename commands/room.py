from timetabletools import TimetableTools
from spreadsheet_data.full_time_semester_event_data import *


class Room:

    def __init__(self):
        self.tools = TimetableTools()

    def equal_time(self, time_first, time_second):
        if time_first is '' or time_second is '':
            return False
        time_first_split = time_first.split(':')
        time_second_split = str(time_second).split(':')

        if int(time_first_split[0]) != int(time_second_split[0]) \
                or int(time_first_split[1]) != int(time_second_split[1]):
            return False
        return True

    def get_room_event_by_day(self, day, time_block, room, data_id, semester_data):
        for event_id in room.referenced_by[data_id]:
            event = semester_data[event_id]

            if event.event_time != 0 \
                    and day == event.day_name \
                    and self.equal_time(time_block, event.start_time):

                print("time:", event.event_time.get_string())
                print("id:", event.course_id)
                print("week name:", event.week_name)
                print("type:", event_types[event.event_type])
                print("trainer_id:", event.trainer_id)

    def exec_command(self, spreadsheet_data, args):
        print("start")
        for room_key, room in spreadsheet_data.room_data.data.items():
            print("Sala:", str(room.building_id) + ' - ' + str(room.name) + "\n")
            for day in self.tools.days_of_week[0:5]:
                print(self.tools.days_of_week_label[day])

                data_id = id(spreadsheet_data.full_time_first_semester_event_data)
                semester_data = spreadsheet_data.full_time_first_semester_event_data.data

                if data_id not in room.referenced_by:
                    continue

                for time_block in self.tools.time_blocks:
                    self.get_room_event_by_day(day, time_block, room, data_id, semester_data)

                print("+++")
            print("------------------------------------------")

