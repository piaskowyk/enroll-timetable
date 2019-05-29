class DepartmentInfo:
    name = ''

    def __init__(self, name):
        self.name = name


class DepartmentData:
    data = dict()

    def __init__(self):
        pass

    def get_department_id(self, department_name):
        if department_name in self.data:
            return department_name
        new_info = DepartmentInfo(department_name)
        self.data[department_name] = new_info
        return department_name
