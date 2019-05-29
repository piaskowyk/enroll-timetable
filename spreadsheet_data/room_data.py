from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter

room_types = {'0': 'Undefined type of room',
              'W': 'Lecture room',
              'C': 'Practice room',
              'L': 'Laboratory room'}


class RoomInfo:
    building_id = 0
    name = ""
    type = '0'
    capacity = 0
    comments = ""
    full_time_first_events = []
    full_time_second_events = []
    other_first_events = []
    other_second_events = []

    def __init__(self, record, building_data):
        self.name = record['roomName']
        self.type = record['roomType']
        self.capacity = record['capacity']
        self.comments = record['comments']
        self.building_id = building_data.get_building_id(
            record['buildingName'])


class RoomData:
    data = dict()

    def __init__(self, config, workbook, building_data):
        rooms_data_importer = SpreadsheetDataImporter(config, workbook, "rooms")
        cur_record = rooms_data_importer.load_next_record()
        while len(cur_record) > 0:
            cur_room = RoomInfo(cur_record, building_data)
            self.data[str(cur_record['buildingName']) + ":" +
                      str(cur_room.name)] = cur_room
            cur_record = rooms_data_importer.load_next_record()

    def get_room_id(self, building_name, room_name):
        key = building_name + ':' + room_name
        if key in self.data:
            return key
        else:
            raise NameError(
                'Romm ' + room_name + ' in ' + building_name + ' not found!\n')
