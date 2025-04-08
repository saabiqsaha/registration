import csv
import os
from student import Student
from course import Course

class EnrollmentSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.load_data()

    def load_data(self):
        if os.path.exists("students.csv"):
            with open("students.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    student_id, name, *courses = row
                    student = Student(student_id, name)
                    student.registered_courses = set(courses)
                    self.students[student_id] = student

        if os.path.exists("courses.csv"):
            with open("courses.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    course_id, name, instructor, *students = row
                    course = Course(course_id, name, instructor)
                    course.enrolled_students = set(students)
                    self.courses[course_id] = course

    def save_data(self):
        with open("students.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                writer.writerow([student.student_id, student.name] + list(student.registered_courses))

        with open("courses.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor] + list(course.enrolled_students))

        with open("enrollments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                for course_id in student.registered_courses:
                    writer.writerow([student.student_id, course_id])

    def register_student(self, student_id, name):
        if student_id in self.students:
            return False, "Student ID already exists"
        else:
            self.students[student_id] = Student(student_id, name)
            self.save_data()
            return True, "Student registered successfully"

    def add_course(self, course_id, name, instructor):
        if course_id in self.courses:
            return False, "Course ID already exists"
        else:
            self.courses[course_id] = Course(course_id, name, instructor)
            self.save_data()
            return True, "Course added successfully"

    def enroll_student(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            return False, "Invalid student or course ID"

        student = self.students[student_id]
        course = self.courses[course_id]

        if len(course.enrolled_students) >= course.max_students:
            return False, "Course is full"

        if course_id in student.registered_courses:
            return False, "Student already enrolled in this course"

        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        self.save_data()
        return True, "Enrollment successful"

    def drop_course(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            return False, "Invalid student or course ID"

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.registered_courses:
            student.registered_courses.remove(course_id)
            course.enrolled_students.discard(student_id)
            self.save_data()
            return True, "Course dropped successfully"
        else:
            return False, "Student is not enrolled in this course"

    def get_available_courses(self):
        available_courses = []
        for course_id, course in self.courses.items():
            enrollment = f"{len(course.enrolled_students)}/{course.max_students}"
            available_courses.append({
                'id': course_id,
                'name': course.name,
                'instructor': course.instructor,
                'enrollment': enrollment
            })
        return available_courses
    
    def get_student_courses(self, student_id):
        if student_id not in self.students:
            return []
        
        student_courses = []
        for course_id in self.students[student_id].registered_courses:
            if course_id in self.courses:
                course = self.courses[course_id]
                student_courses.append({
                    'id': course_id,
                    'name': course.name,
                    'instructor': course.instructor
                })
        return student_courses 