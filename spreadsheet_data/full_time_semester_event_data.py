from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter
from spreadsheet_data.common_data import *
from interface_tools.output_tools import *

# dictionary with possible types of events used in spreadsheet
event_types = {'W': 'Lecture',
               'C': 'Practice exercises',
               'L': 'Laboratory exercises',
               'E': 'Exam',
               'P': 'Unknown1',
               'D': 'Unknown2',
               'OK': 'Final grade'}


class FullTimeSemesterEventInfo:
    # class for one full-time semester event record

    # initiates object with information provided in record
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

        # if at least one of columns with weekly time period is empty
        if record['day'] is None or \
                record['startTime'] is None:
            self.event_time = 0
        else:
            # if it is our department's event block
            if record['endTime'] is None:
                self.event_time = WeeklyTimePeriod(record['day'],
                                                   record['startTime'])
            # if it is customised weekly time period
            else:
                self.event_time = WeeklyTimePeriod(record['day'],
                                                   record['startTime'],
                                                   record['endTime'])
        self.start_time = record['startTime']
        self.day_name = record['day']
        self.unknown = record['unknown']
        self.comments = record['comments']

        # gets primary key of record with provided course
        self.course_id = course_data.get_course_id(record['studies'],
                                                   record['semester'],
                                                   record['course'],
                                                   record['electiveId'],
                                                   requester_data,
                                                   self.get_key())

        # gets primary key of record with provided department (if set)
        if record['departmentName'] is None:
            self.department_id = 0
        else:
            self.department_id = department_data.get_department_id(
                record['departmentName'], requester_data, self.get_key())

        # gets primary key of record with provided trainer (if valid)
        if record['trainer'] is None or len(record['trainer'].split()) != 2:
            self.trainer_id = 0
        else:
            self.trainer_id = trainer_data.get_trainer_id(
                record['trainer'].split()[-1],
                record['trainer'].split()[0: -1], requester_data,
                self.get_key())

        # gets primary key of record with provided room (if valid)
        if record['roomName'] is None or len(record['roomName'].split()) != 2:
            self.room_id = 0
        else:
            self.room_id = room_data.get_room_id(record['roomName'].split()[0],
                                                 record['roomName'].split()[1],
                                                 requester_data, self.get_key())

    # returns primary key
    def get_key(self):
        return self.event_id

    # remember object, that references to this record, from particular data
    # table
    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class FullTimeSemesterEventData:
    # class for table with records about full-time semester events

    def __init__(self, config, workbook, semester, course_data, department_data,
                 trainer_data, room_data):
        self.data = dict()

        # prepares to import data from spreadsheet
        event_data_importer = SpreadsheetDataImporter(config, workbook,
                                                      semester)
        cur_record = event_data_importer.load_next_record()
        null_records_to_stop = 20
        cur_null_records_to_stop = null_records_to_stop

        # do until max limit of empty rows is reached
        while cur_null_records_to_stop > 0:
            # if not empty record was loaded
            if len(cur_record) > 0:
                cur_null_records_to_stop = null_records_to_stop
                if cur_record['course'] is not None:
                    cur_event = FullTimeSemesterEventInfo(cur_record,
                                                          len(self.data),
                                                          course_data,
                                                          department_data,
                                                          trainer_data,
                                                          room_data,
                                                          self)

                    # show errors in case of invalid data in spreadsheet row
                    if cur_record['eventType'] not in event_types:
                        show_warning(
                            event_data_importer.get_last_record_info() +
                            ': Event type is not valid.')
                    if cur_event.trainer_id is None:
                        show_error(
                            event_data_importer.get_last_record_info() +
                            ': Trainer ' + cur_record['trainer'] +
                            ' not found.')
                    if cur_event.room_id is None:
                        show_error(
                            event_data_importer.get_last_record_info() +
                            ': Room \"' + cur_record['roomName'] +
                            '\" not found.')
                    if cur_record['day'] is None or \
                            cur_record['startTime'] is None:
                        show_warning(
                            event_data_importer.get_last_record_info() +
                            ': Event time is not set.')

                    # adds record to table
                    self.data[cur_event.get_key()] = cur_event
            else:
                cur_null_records_to_stop -= 1
            cur_record = event_data_importer.load_next_record()
