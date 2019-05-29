class CourseInfo:
    studies = ''
    semester = ''
    name = ''
    elective_id =''

    def __init__(self, studies, semester, name, elective_id):
        self.studies = studies
        self.semester = semester
        self.name = name
        self.elective_id = elective_id


class CourseData:
    data = dict()

    def __init__(self):
        pass

    def get_course_id(self, studies, semester, course_name, elective_id):
        if course_name in self.data:
            return course_name
        new_info = CourseInfo(studies, semester, course_name, elective_id)
        self.data[course_name] = new_info
        return course_name
