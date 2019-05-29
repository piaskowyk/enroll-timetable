class DepartmentInfo:
    name = ''
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


class DepartmentData:
    data = dict()

    def __init__(self):
        pass

    def get_department_id(self, department_name, requester_data, requester_key):
        if department_name in self.data:
            self.data[department_name].add_reference(requester_data,
                                                     requester_key)
            return department_name
        new_info = DepartmentInfo(department_name)
        self.data[department_name] = new_info
        self.data[department_name].add_reference(requester_data, requester_key)
        return department_name
