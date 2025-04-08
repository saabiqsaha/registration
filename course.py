class Course:
    def __init__(self, course_id, name, instructor, max_students=30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students 