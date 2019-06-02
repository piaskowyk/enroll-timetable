class BuildingInfo:
    name = ""
    referenced_by = dict()

    def __init__(self, name):
        self.referenced_by = dict()
        self.name = name

    def get_key(self):
        return str(self.name)

    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class BuildingData:
    data = 0

    def __init__(self):
        self.data = dict()
        pass

    def get_building_id(self, building_name, requester_data, requester_key):
        if building_name in self.data:
            self.data[building_name].add_reference(requester_data,
                                                   requester_key)
            return building_name
        new_info = BuildingInfo(building_name)
        self.data[new_info.get_key()] = new_info
        self.data[building_name].add_reference(requester_data, requester_key)
        return building_name
