from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter
from interface_tools.output_tools import *

# dictionary of room types used in spreadsheet
room_types = {'W': 'Lecture room',
              'C': 'Practice room',
              'L': 'Laboratory room'}


class RoomInfo:
    # class for one room record

    # initiates object with information provided in record
    def __init__(self, record, building_data, requester_data):
        self.referenced_by = dict()
        self.name = record['roomName']
        self.type = record['roomType']
        self.capacity = record['capacity']
        self.comments = record['comments']
        self.building_id = record['buildingName']

        # gets primary key of record with provided building
        self.building_id = building_data.get_building_id(
            record['buildingName'], requester_data, self.get_key())

    # returns primary key
    def get_key(self):
        return str(self.building_id) + ':' + str(self.name)

    # remember object, that references to this record, from particular data
    # table
    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class RoomData:
    # class for table with records about rooms

    # building table with records about rooms from workbook
    def __init__(self, config, workbook, building_data):
        self.data = dict()

        # prepares to import data from spreadsheet
        rooms_data_importer = SpreadsheetDataImporter(config, workbook, "rooms")
        cur_record = rooms_data_importer.load_next_record()

        # until empty record is loaded
        while len(cur_record) > 0:
            cur_room = RoomInfo(cur_record, building_data, self)

            # show errors, warnings and weak warnings in case of invalid data
            # in spreadsheet row
            if cur_record['roomName'] is None:
                show_error(rooms_data_importer.get_last_record_info() +
                           ': Room name is not set. ')
            if cur_record['roomType'] not in room_types:
                show_warning(rooms_data_importer.get_last_record_info() +
                             ': Room type is not valid. ')
            if cur_record['capacity'] is None:
                show_weak_warning(rooms_data_importer.get_last_record_info() +
                                  ': Room capacity not set. ')

            # adds record to table
            self.data[str(cur_record['buildingName']) + ':' +
                      str(cur_room.name)] = cur_room
            cur_record = rooms_data_importer.load_next_record()

    # returns primary key of this record; if information about provided room
    # doesn't exist returns None
    def get_room_id(self, building_name, room_name, requester_data,
                    requester_key):
        key = building_name + ':' + room_name
        if key in self.data:
            self.data[key].add_reference(requester_data, requester_key)
            return key
        else:
            return None
