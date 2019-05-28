class DepartmentInfo:
    id = 0
    name = ''

    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name


class DepartmentData:
    data = dict()

    def __init__(self):
        pass

    def get_department_id(self, department_name):
        if department_name in self.data:
            return self.data[department_name].id
        new_info = DepartmentInfo(len(self.data), department_name)
        self.data[department_name] = new_info
        return self.data[department_name].id
