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
            'day': None,
            'hour': None,
            'room': None,
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

    def exec_command(self, spreadsheet_data, args):
        if self.args_val['room'] is not None:
            self.find_free_times_in_room(spreadsheet_data, args)
        else:
            self.find_free_rooms_in_time(spreadsheet_data, args)

    def parse_args(self, args):
        for i, item in enumerate(args):
            if item in self.args.keys() and i + 1 < len(args):
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

    def find_free_rooms_in_time(self, spreadsheet_data, args):
        self.parse_args(args)
        rooms_details = self.get_room_event_list(spreadsheet_data)

        if self.args_val['hour'] is not None \
                and self.args_val['hour'] not in self.tools.time_blocks.keys():
            print("Invalid time format")
            return

        if self.args_val['day'] is not None \
                and self.args_val['day'] not in self.tools.days_of_week_label.keys():
            print("Invalid day format")
            return

        d_name = str(self.args_val['day'])
        if self.args_val['day'] is None:
            d_name = '-'

        h_name = str(self.args_val['hour'])
        if self.args_val['hour'] is None:
            h_name = '-'

        print("Free room at: day: " + d_name + " hour: " + h_name)
        for room_key, room in rooms_details.items():

            print(spreadsheet_data.room_data.data[room_key].type)

            if self.args_val['capacity'] is not None:
                if spreadsheet_data.room_data.data[room_key].capacity < self.args_val['capacity']:
                    continue

            if self.args_val['type'] is not None:
                if spreadsheet_data.room_data.data[room_key].type != self.args_val['type']:
                    continue

            if self.args_val['day'] is not None:
                day = room[self.args_val['day']]
                if day is None:
                    continue

                if self.args_val['hour'] is not None:
                    if day[self.args_val['hour']] is None:
                        print("Free room: ", room_key)
                else:
                    for key, event in room[self.args_val['day']].items():
                        if event is None:
                            print("Free room: " + room_key + " " + key)
            else:
                for day_key, day_info in room.items():
                    if day_info is None:
                        continue

                    if self.args_val['hour'] is not None:
                        if day_info[self.args_val['hour']] is None:
                            print("Free room: " + room_key + " " + day_key)
                    else:
                        for key, event in day_info.items():
                            if event is None:
                                print("Free room: " + room_key + " " + day_key + " " + key)

    def find_free_times_in_room(self, spreadsheet_data, args):
        self.parse_args(args)
        rooms_details = self.get_room_event_list(spreadsheet_data)

        if self.args_val['room'] is None:
            print("You must type room name")
            return

        room_name = self.args_val['room']
        # print(rooms_details.keys())
        print(room_name)
        if room_name not in rooms_details.keys():
            print("This room not exist")
            return

        if self.args_val['capacity'] is not None:
            if spreadsheet_data.room_data.data[room_name].capacity < self.args_val['capacity']:
                print("This room is too small")
                return

        if self.args_val['type'] is not None:
            if spreadsheet_data.room_data.data[room_name].type != self.args_val['type']:
                print("This room have different type")
                return

        room = rooms_details[room_name]
        for day_key, day_info in room.items():
            if day_info is None:
                continue
            for key, event in day_info.items():
                if event is None:
                    print("Free room: " + day_key + " " + key)
