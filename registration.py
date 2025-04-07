import csv
import os

# ---------- Student Class ----------
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.registered_courses = set()

# ---------- Course Class ----------
class Course:
    def __init__(self, course_id, name, instructor, max_students=30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students

# ---------- Enrollment System ----------
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
            print("⚠️ Student already exists.")
        else:
            self.students[student_id] = Student(student_id, name)
            print("✅ Student registered.")
            self.save_data()

    def add_course(self, course_id, name, instructor):
        if course_id in self.courses:
            print("⚠️ Course already exists.")
        else:
            self.courses[course_id] = Course(course_id, name, instructor)
            print("✅ Course added.")
            self.save_data()

    def enroll_student(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            print("⚠️ Invalid student or course ID.")
            return

        student = self.students[student_id]
        course = self.courses[course_id]

        if len(course.enrolled_students) >= course.max_students:
            print("❌ Course is full.")
            return

        if course_id in student.registered_courses:
            print("⚠️ Student already enrolled.")
            return

        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        print("✅ Enrollment successful.")
        self.save_data()

    def drop_course(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            print("⚠️ Invalid student or course ID.")
            return

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.registered_courses:
            student.registered_courses.remove(course_id)
            course.enrolled_students.discard(student_id)
            print("✅ Course dropped.")
            self.save_data()
        else:
            print("⚠️ Student is not enrolled in this course.")

    def view_available_courses(self):
        print("\n📚 Available Courses:")
        for course_id, course in self.courses.items():
            print(f"{course_id} - {course.name} | Instructor: {course.instructor} | Enrolled: {len(course.enrolled_students)}/{course.max_students}")
        print()

# ---------- CLI ----------
def main():
    system = EnrollmentSystem()

    while True:
        print("\n🎓 UNIVERSITY COURSE REGISTRATION SYSTEM")
        print("1. Register a new student")
        print("2. Add a new course")
        print("3. Enroll a student in a course")
        print("4. Drop a course for a student")
        print("5. View all available courses")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            name = input("Enter student name: ").strip()
            system.register_student(student_id, name)

        elif choice == "2":
            course_id = input("Enter course ID: ").strip()
            name = input("Enter course name: ").strip()
            instructor = input("Enter instructor name: ").strip()
            system.add_course(course_id, name, instructor)

        elif choice == "3":
            student_id = input("Enter student ID: ").strip()
            course_id = input("Enter course ID to enroll: ").strip()
            system.enroll_student(student_id, course_id)

        elif choice == "4":
            student_id = input("Enter student ID: ").strip()
            course_id = input("Enter course ID to drop: ").strip()
            system.drop_course(student_id, course_id)

        elif choice == "5":
            system.view_available_courses()

        elif choice == "6":
            print("👋 Exiting system. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from 1 to 6.")

# ---------- Run the CLI ----------
if __name__ == "__main__":
    main()
