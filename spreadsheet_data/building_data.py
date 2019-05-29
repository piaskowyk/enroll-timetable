class BuildingInfo:
    name = ""

    def __init__(self, name):
        self.name = name


class BuildingData:
    data = dict()

    def __init__(self):
        pass

    def get_building_id(self, building_name):
        if building_name in self.data:
            return building_name
        new_info = BuildingInfo(building_name)
        self.data[building_name] = new_info
        return building_name
