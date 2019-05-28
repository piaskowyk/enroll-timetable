from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter

room_types = {'0': 'Undefined type of room',
              'W': 'Lecture room',
              'C': 'Practice room',
              'L': 'Laboratory room'}


class RoomInfo:
    id = 0
    building_id = 0
    name = ""
    type = '0'
    capacity = 0
    comments = ""

    def __init__(self, identifier, record, building_data):
        self.id = identifier
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
            cur_room = RoomInfo(len(self.data), cur_record, building_data)
            self.data[str(cur_record['buildingName']) + ":" +
                      str(cur_room.name)] = cur_room
            cur_record = rooms_data_importer.load_next_record()
