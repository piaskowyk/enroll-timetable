from utils.timetabletools import TimetableTools


def equal_time(time_first, time_second):
    if time_first is '' or time_second is '':
        return False
    time_first_split = time_first.split(':')
    time_second_split = str(time_second).split(':')

    if int(time_first_split[0]) != int(time_second_split[0]) \
            or int(time_first_split[1]) != int(time_second_split[1]):
        return False
    return True


class FreeRoomInfo:
    def __init__(self):
        self.room = ''
        self.free_terms = dict()

    def add_free_terms(self, day, hour):
        if day not in self.free_terms.keys():
            self.free_terms[day] = list()
        self.free_terms[day].append(hour)


class FreeRoom:

    def __init__(self):
        self.tools = TimetableTools()
        self.room_events = None
        self.data_id = None
        self.args_val = {
            'day': [],
            'hour': [],
            'room': [],
            'capacity': None,
            'type': None
        }
        self.args = {
            '-d': 'day',
            '-h': 'hour',
            '-r': 'room',
            '-c': 'capacity',
            '-t': 'type'
        }
        self.args_can_many = {
            "-r",
            "-d",
            "-h"
        }

    def exec_command(self, spreadsheet_data, args):
        self.parse_args(args)
        rooms_details = self.get_room_event_list(spreadsheet_data)
        # print(rooms_details)
        print("Free room")
        print("day:", self.args_val['day'])
        print("hour:", self.args_val['hour'])
        print("room:", self.args_val['room'])
        print("capacity:", self.args_val['capacity'])
        print("type:", self.args_val['type'])
        print("--------------------------")

        if len(self.args_val['room']) > 0:
            rooms_name = self.args_val['room']
            for item in rooms_name:
                if item not in rooms_details.keys():
                    print("This room not exist,", item)
                    return
            rooms_details = {key: room for key, room in rooms_details.items() if key in self.args_val['room']}

        if len(self.args_val['day']) > 0:
            days = self.args_val['day']
            for item in days:
                if item not in self.tools.days_of_week_label.keys():
                    print("This day not exist,", item)
                    return

        if len(self.args_val['hour']) > 0:
            hours = self.args_val['hour']
            for item in hours:
                if item not in self.tools.time_blocks.keys():
                    print("Invalid time format", item)
                    return

        for room_key, room in rooms_details.items():

            if self.args_val['capacity'] is not None:
                if spreadsheet_data.room_data.data[room_key].capacity < self.args_val['capacity']:
                    continue

            if self.args_val['type'] is not None:
                if spreadsheet_data.room_data.data[room_key].type != self.args_val['type']:
                    continue

            print("Room", room_key)

            if len(self.args_val['day']) > 0:
                for item in self.args_val['day']:
                    day = room[item]
                    if day is None:
                        continue

                    print("Day", item)

                    if len(self.args_val['hour']) > 0:
                        for hour in self.args_val['hour']:
                            if day[hour] is None:
                                print("Free room: ", room_key, hour)
                    else:
                        for key, event in room[item].items():
                            if event is None:
                                print("Free room: " + room_key + " " + key)
            else:
                for day_key, day_info in room.items():
                    if day_info is None:
                        continue

                    if len(self.args_val['hour']) > 0:
                        for hour in self.args_val['hour']:
                            if day_info[hour] is None:
                                print("Free room: " + room_key + " " + day_key, hour)
                    else:
                        for key, event in day_info.items():
                            if event is None:
                                print("Free room: " + room_key + " " + day_key + " " + key)

    def parse_args(self, args):
        for i, item in enumerate(args):
            if item in self.args.keys() and i + 1 < len(args):
                if item in self.args_can_many:
                    self.args_val[self.args[item]].append(args[i + 1])
                else:
                    self.args_val[self.args[item]] = args[i + 1]

    def get_room_event_by_day(self, room, data_id, semester_data):
        event_data = dict()
        for event_id in room.referenced_by[data_id]:
            event = semester_data[event_id]
            if event.event_time is 0:
                continue
            time_start = event.event_time.get_string().split(' ')[1]
            event_data[time_start] = [
                time_start,
                event.course_id,
                event.week_name,
                event.event_type,
                event.trainer_id
            ]

        for time_key in self.tools.time_blocks.keys():
            if time_key not in event_data.keys():
                event_data[time_key] = None

        return event_data

    def get_room_event_list(self, spreadsheet_data):
        if self.room_events is not None and id(spreadsheet_data) is self.data_id:
            return self.room_events

        self.data_id = id(spreadsheet_data)
        self.room_events = dict()
        for room_key, room in spreadsheet_data.room_data.data.items():
            day_event = dict()
            for day in self.tools.days_of_week[0:5]:
                data_id = id(spreadsheet_data.full_time_first_semester_event_data)
                semester_data = spreadsheet_data.full_time_first_semester_event_data.data

                result = None
                if data_id in room.referenced_by:
                    result = self.get_room_event_by_day(room, data_id, semester_data)
                day_event[day] = result
            self.room_events[room_key] = day_event

        return self.room_events
