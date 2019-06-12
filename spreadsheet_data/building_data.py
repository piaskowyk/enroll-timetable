class BuildingInfo:
    # class for one building record

    def __init__(self, name):
        self.referenced_by = dict()
        self.name = name

    # returns primary key
    def get_key(self):
        return str(self.name)

    # remember object, that references to this record, from particular data
    # table
    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class BuildingData:
    # class for table with records about buildings

    def __init__(self):
        self.data = dict()

    # adds to table new record about building if record doesn't exists and
    # returns primary key of this record
    def get_building_id(self, building_name, requester_data, requester_key):
        if building_name in self.data:
            self.data[building_name].add_reference(requester_data,
                                                   requester_key)
            return building_name
        new_info = BuildingInfo(building_name)
        self.data[new_info.get_key()] = new_info
        self.data[building_name].add_reference(requester_data, requester_key)
        return building_name
