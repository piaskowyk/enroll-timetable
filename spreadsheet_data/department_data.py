class DepartmentInfo:
    # class for one department record

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


class DepartmentData:
    # class for table with records about buildings

    def __init__(self):
        self.data = dict()

    # adds to table new record about department if record doesn't exists and
    # returns primary key of this record
    def get_department_id(self, department_name, requester_data, requester_key):
        if department_name in self.data:
            self.data[department_name].add_reference(requester_data,
                                                     requester_key)
            return department_name
        new_info = DepartmentInfo(department_name)
        self.data[department_name] = new_info
        self.data[department_name].add_reference(requester_data, requester_key)
        return department_name
