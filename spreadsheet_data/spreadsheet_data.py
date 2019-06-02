from spreadsheet_data.building_data import *
from spreadsheet_data.room_data import *
from spreadsheet_data.department_data import *
from spreadsheet_data.trainer_data import *
from spreadsheet_data.course_data import *
from spreadsheet_data.full_time_semester_event_data import *


class SpreadsheetData:
    building_data = 0
    room_data = 0
    department_data = 0
    trainer_data = 0
    course_data = 0
    full_time_first_semester_event_data = 0
    full_time_second_semester_event_data = 0

    def __init__(self, config, workbook):
        self.building_data = BuildingData()
        self.room_data = RoomData(config, workbook, self.building_data)
        self.department_data = DepartmentData()
        self.trainer_data = TrainerData(config, workbook,
                                        self.department_data)
        self.course_data = CourseData()
        self.full_time_first_semester_event_data = FullTimeSemesterEventData(
            config, workbook, 'fullTimeFirst', self.course_data,
            self.department_data, self.trainer_data, self.room_data)
        self.full_time_second_semester_event_data = FullTimeSemesterEventData(
            config, workbook, 'fullTimeSecond', self.course_data,
            self.department_data, self.trainer_data, self.room_data)
