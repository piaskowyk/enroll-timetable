class CourseInfo:
    studies = ''
    semester = ''
    name = ''
    elective_id = ''
    referenced_by = dict()

    def __init__(self, studies, semester, name, elective_id):
        self.referenced_by = dict()
        self.studies = studies
        self.semester = semester
        self.name = name
        self.elective_id = elective_id

    def get_key(self):
        return str(self.name)

    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class CourseData:
    data = dict()

    def __init__(self):
        pass

    def get_course_id(self, studies, semester, course_name, elective_id,
                      requester_data, requester_key):
        if course_name in self.data:
            self.data[course_name].add_reference(requester_data, requester_key)
            return course_name
        new_info = CourseInfo(studies, semester, course_name, elective_id)
        self.data[course_name] = new_info
        self.data[course_name].add_reference(requester_data, requester_key)
        return course_name
