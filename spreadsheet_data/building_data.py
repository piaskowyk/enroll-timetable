class BuildingInfo:
    id = 0
    name = ""

    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name


class BuildingData:
    data = dict()

    def __init__(self):
        pass

    def get_building_id(self, building_name):
        if building_name in self.data:
            return self.data[building_name].id
        new_info = BuildingInfo(len(self.data), building_name)
        self.data[building_name] = new_info
        return self.data[building_name].id
