class CourseInfo:
    # class for one course record

    def __init__(self, studies, semester, name, elective_id):
        self.referenced_by = dict()
        self.studies = studies
        self.semester = semester
        self.name = name
        self.elective_id = elective_id

    # returns primary key
    def get_key(self):
        return str(self.name)

    # remember object, that references to this record, from particular data
    # table
    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class CourseData:
    # class for table with records about courses

    def __init__(self):
        self.data = dict()

    # adds to table new record about course if record doesn't exists and
    # returns primary key of this record
    def get_course_id(self, studies, semester, course_name, elective_id,
                      requester_data, requester_key):
        if course_name in self.data:
            self.data[course_name].add_reference(requester_data, requester_key)
            return course_name
        new_info = CourseInfo(studies, semester, course_name, elective_id)
        self.data[course_name] = new_info
        self.data[course_name].add_reference(requester_data, requester_key)
        return course_name
