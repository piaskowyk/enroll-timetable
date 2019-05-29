from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter
from spreadsheet_data.common_data import *

event_types = {'0': 'Undefined type of event',
               'W': 'Lecture',
               'C': 'Practice exercises',
               'L': 'Laboratory exercises'}


class FullTimeSemesterEventInfo:
    event_id = 0
    course_id = ''
    localization = ''
    event_type = ''
    group_name = ''
    hours_number = 0
    executed_hours_number = 0
    department_id = ''
    trainer_id = ''
    room_id = ''
    week_name = ''
    event_time = 0
    unknown = ''
    comments = ''
    referenced_by = dict()

    def __init__(self, record, event_id, course_data, department_data,
                 trainer_data, room_data, requester_data):
        self.referenced_by = dict()
        self.event_id = event_id
        self.localization = record['localization']
        self.event_type = record['eventType']
        self.group_name = record['groupName']
        self.hours_number = record['hoursNumber']
        self.executed_hours_number = record['executedHoursNumber']
        self.week_name = record['weekName']
        if record['day'] is None or \
                record['startTime'] is None:
            self.event_time = 0
        else:
            if record['endTime'] is None:
                self.event_time = WeeklyTimePeriod(record['day'],
                                                   record['startTime'])
            else:
                self.event_time = WeeklyTimePeriod(record['day'],
                                                   record['startTime'],
                                                   record['endTime'])
        self.unknown = record['unknown']
        self.comments = record['comments']
        self.course_id = course_data.get_course_id(record['studies'],
                                                   record['semester'],
                                                   record['course'],
                                                   record['electiveId'],
                                                   requester_data,
                                                   self.get_key())
        if record['departmentName'] is None:
            self.department_id = 0
        else:
            self.department_id = department_data.get_department_id(
                record['departmentName'], requester_data, self.get_key())
        if record['trainer'] is None or len(record['trainer'].split()) != 2:
            self.trainer_id = 0
        else:
            self.trainer_id = trainer_data.get_trainer_id(
                record['trainer'].split()[-1],
                record['trainer'].split()[0: -1], requester_data,
                self.get_key())
        if record['roomName'] is None or len(record['roomName'].split()) != 2:
            self.room_id = 0
        else:
            self.room_id = room_data.get_room_id(record['roomName'].split()[0],
                                                 record['roomName'].split()[1],
                                                 requester_data, self.get_key())

    def get_key(self):
        return self.event_id

    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class FullTimeSemesterEventData:
    data = dict()

    def __init__(self, config, workbook, semester, course_data, department_data,
                 trainer_data, room_data):
        event_data_importer = SpreadsheetDataImporter(config, workbook,
                                                      semester)
        cur_record = event_data_importer.load_next_record()
        while len(cur_record) > 0:
            cur_event = FullTimeSemesterEventInfo(cur_record, len(self.data),
                                                  course_data, department_data,
                                                  trainer_data, room_data,
                                                  self)
            self.data[cur_event.get_key()] = cur_event
            cur_record = event_data_importer.load_next_record()