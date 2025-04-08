import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.registered_courses = set()


class Course:
    def __init__(self, course_id, name, instructor, max_students=30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students


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
                    if row:
                        student_id, name, *courses = row
                        student = Student(student_id, name)
                        student.registered_courses = set(courses) if courses else set()
                        self.students[student_id] = student

        if os.path.exists("courses.csv"):
            with open("courses.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:  
                        course_id, name, instructor, max_students, *students = row
                        course = Course(course_id, name, instructor, int(max_students))
                        course.enrolled_students = set(students) if students else set()
                        self.courses[course_id] = course
        
       
        for student in self.students.values():
            
            invalid_courses = [course_id for course_id in student.registered_courses 
                              if course_id not in self.courses]
            for course_id in invalid_courses:
                student.registered_courses.remove(course_id)
        
        
        for course in self.courses.values():
            
            invalid_students = [student_id for student_id in course.enrolled_students 
                               if student_id not in self.students]
            for student_id in invalid_students:
                course.enrolled_students.discard(student_id)

    def save_data(self):
        with open("students.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                writer.writerow([student.student_id, student.name] + list(student.registered_courses))

        with open("courses.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor, course.max_students] + list(course.enrolled_students))

        with open("enrollments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                for course_id in student.registered_courses:
                    writer.writerow([student.student_id, course_id])

    def register_student(self, student_id, name):
        if student_id in self.students:
            return False, "Student already exists."
        self.students[student_id] = Student(student_id, name)
        self.save_data()
        return True, "Student registered successfully."

    def add_course(self, course_id, name, instructor, max_students=30):
        if course_id in self.courses:
            return False, "Course already exists."
        self.courses[course_id] = Course(course_id, name, instructor, max_students)
        self.save_data()
        return True, "Course added successfully."

    def enroll_student(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            return False, "Invalid student or course ID."

        student = self.students[student_id]
        course = self.courses[course_id]

        if len(course.enrolled_students) >= course.max_students:
            return False, "Course is full."

        if course_id in student.registered_courses:
            return False, "Student already enrolled in this course."

        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        self.save_data()
        return True, "Enrollment successful."

    def drop_course(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            return False, "Invalid student or course ID."

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.registered_courses:
            student.registered_courses.remove(course_id)
            course.enrolled_students.discard(student_id)
            self.save_data()
            return True, "Course dropped successfully."
        else:
            return False, "Student is not enrolled in this course."

    def get_available_courses(self):
        return [(course_id, course.name, course.instructor, 
                len(course.enrolled_students), course.max_students) 
                for course_id, course in self.courses.items()]
    
    def get_student_courses(self, student_id):
        if student_id not in self.students:
            return []
        
        student = self.students[student_id]
        return [(course_id, self.courses[course_id].name, self.courses[course_id].instructor)
                for course_id in student.registered_courses if course_id in self.courses]

# Graphical User Interface
class UniversityRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Registration System")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        self.system = EnrollmentSystem()
        self.current_student = None
        
        self.setup_ui()
        
    def setup_ui(self):
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        self.login_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.login_frame, text="Login / Register")
        self.setup_login_ui()
        
        
        self.courses_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.courses_frame, text="Course Registration")
        self.setup_courses_ui()
        
        self.admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_frame, text="Admin")
        self.setup_admin_ui()
        
        self.notebook.tab(1, state="disabled")
        
    def setup_login_ui(self):
        login_container = ttk.Frame(self.login_frame, padding=20)
        login_container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(login_container, text="Welcome to University Course Registration", 
                  font=("Helvetica", 16)).pack(pady=20)
        
        ttk.Label(login_container, text="Student ID:").pack(anchor=tk.W, pady=(10, 0))
        self.student_id_entry = ttk.Entry(login_container, width=30)
        self.student_id_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(login_container, text="Student Name:").pack(anchor=tk.W, pady=(10, 0))
        self.student_name_entry = ttk.Entry(login_container, width=30)
        self.student_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(login_container)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.handle_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Register", command=self.handle_register).pack(side=tk.LEFT, padx=5)
        
    def setup_courses_ui(self):
        courses_container = ttk.Frame(self.courses_frame, padding=20)
        courses_container.pack(fill=tk.BOTH, expand=True)
        
        self.student_info_label = ttk.Label(courses_container, text="Not logged in", font=("Helvetica", 12))
        self.student_info_label.pack(anchor=tk.W, pady=(0, 20))
        
        course_notebook = ttk.Notebook(courses_container)
        course_notebook.pack(fill=tk.BOTH, expand=True)
        
        available_frame = ttk.Frame(course_notebook)
        course_notebook.add(available_frame, text="Available Courses")
        
        self.available_courses_tree = ttk.Treeview(available_frame, columns=("ID", "Name", "Instructor", "Enrolled", "Capacity"), show="headings")
        self.available_courses_tree.heading("ID", text="Course ID")
        self.available_courses_tree.heading("Name", text="Course Name")
        self.available_courses_tree.heading("Instructor", text="Instructor")
        self.available_courses_tree.heading("Enrolled", text="Enrolled")
        self.available_courses_tree.heading("Capacity", text="Capacity")
        
        self.available_courses_tree.column("ID", width=80)
        self.available_courses_tree.column("Name", width=200)
        self.available_courses_tree.column("Instructor", width=150)
        self.available_courses_tree.column("Enrolled", width=80)
        self.available_courses_tree.column("Capacity", width=80)
        
        scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.available_courses_tree.yview)
        self.available_courses_tree.configure(yscroll=scrollbar.set)
        self.available_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(available_frame, text="Enroll in Selected Course", command=self.handle_enrollment).pack(pady=10)
        
        enrolled_frame = ttk.Frame(course_notebook)
        course_notebook.add(enrolled_frame, text="My Courses")
        
        self.enrolled_courses_tree = ttk.Treeview(enrolled_frame, columns=("ID", "Name", "Instructor"), show="headings")
        self.enrolled_courses_tree.heading("ID", text="Course ID")
        self.enrolled_courses_tree.heading("Name", text="Course Name")
        self.enrolled_courses_tree.heading("Instructor", text="Instructor")
        
        self.enrolled_courses_tree.column("ID", width=80)
        self.enrolled_courses_tree.column("Name", width=200)
        self.enrolled_courses_tree.column("Instructor", width=150)
        
        enrolled_scrollbar = ttk.Scrollbar(enrolled_frame, orient=tk.VERTICAL, command=self.enrolled_courses_tree.yview)
        self.enrolled_courses_tree.configure(yscroll=enrolled_scrollbar.set)
        self.enrolled_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        enrolled_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(enrolled_frame, text="Drop Selected Course", command=self.handle_drop_course).pack(pady=10)
        
        button_frame = ttk.Frame(courses_container)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Refresh Course Lists", command=self.refresh_course_lists).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Logout", command=self.handle_logout).pack(side=tk.RIGHT, padx=5)
        
    def setup_admin_ui(self):
        admin_container = ttk.Frame(self.admin_frame, padding=20)
        admin_container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(admin_container, text="Add New Course", font=("Helvetica", 14)).pack(pady=(0, 10))
        
        ttk.Label(admin_container, text="Course ID:").pack(anchor=tk.W, pady=(10, 0))
        self.course_id_entry = ttk.Entry(admin_container)
        self.course_id_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(admin_container, text="Course Name:").pack(anchor=tk.W, pady=(10, 0))
        self.course_name_entry = ttk.Entry(admin_container)
        self.course_name_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(admin_container, text="Instructor:").pack(anchor=tk.W, pady=(10, 0))
        self.instructor_entry = ttk.Entry(admin_container)
        self.instructor_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(admin_container, text="Maximum Students:").pack(anchor=tk.W, pady=(10, 0))
        self.max_students_entry = ttk.Entry(admin_container)
        self.max_students_entry.pack(fill=tk.X, pady=(0, 5))
        self.max_students_entry.insert(0, "30")
        
        ttk.Button(admin_container, text="Add Course", command=self.handle_add_course).pack(pady=10)
    
    def handle_login(self):
        student_id = self.student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Login Error", "Please enter a Student ID")
            return
            
        if student_id in self.system.students:
            self.current_student = student_id
            student_name = self.system.students[student_id].name
            self.student_info_label.config(text=f"Logged in as: {student_name} (ID: {student_id})")
            self.notebook.tab(1, state="normal")
            self.notebook.select(1)
            self.refresh_course_lists()
            messagebox.showinfo("Login Successful", f"Welcome back, {student_name}!")
        else:
            messagebox.showerror("Login Error", "Student ID not found. Please register first.")
    
    def handle_register(self):
        student_id = self.student_id_entry.get().strip()
        student_name = self.student_name_entry.get().strip()
        if not student_id or not student_name:
            messagebox.showerror("Registration Error", "Please enter both Student ID and Name")
            return
        success, message = self.system.register_student(student_id, student_name)
        if success:
            messagebox.showinfo("Registration Successful", message)
            self.current_student = student_id
            self.student_info_label.config(text=f"Logged in as: {student_name} (ID: {student_id})")
            self.notebook.tab(1, state="normal")
            self.notebook.select(1)
            self.refresh_course_lists()
        else:
            messagebox.showerror("Registration Error", message)
    
    def refresh_course_lists(self):
        for item in self.available_courses_tree.get_children():
            self.available_courses_tree.delete(item)
        for item in self.enrolled_courses_tree.get_children():
            self.enrolled_courses_tree.delete(item)
        
        for course in self.system.get_available_courses():
            course_id, name, instructor, enrolled, capacity = course
            self.available_courses_tree.insert("", "end", values=(course_id, name, instructor, f"{enrolled}/{capacity}", capacity))
        
        if self.current_student:
            for course in self.system.get_student_courses(self.current_student):
                course_id, name, instructor = course
                self.enrolled_courses_tree.insert("", "end", values=(course_id, name, instructor))
    
    def handle_enrollment(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
            
        selected_items = self.available_courses_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a course to enroll")
            return
            
        selected_item = selected_items[0]
        course_id = self.available_courses_tree.item(selected_item, "values")[0]
        success, message = self.system.enroll_student(self.current_student, course_id)
        if success:
            messagebox.showinfo("Enrollment", message)
            self.refresh_course_lists()
        else:
            messagebox.showerror("Enrollment Error", message)
    
    def handle_drop_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
            
        selected_items = self.enrolled_courses_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a course to drop")
            return
            
        selected_item = selected_items[0]
        course_id = self.enrolled_courses_tree.item(selected_item, "values")[0]
        success, message = self.system.drop_course(self.current_student, course_id)
        if success:
            messagebox.showinfo("Course Drop", message)
            self.refresh_course_lists()
        else:
            messagebox.showerror("Error", message)
    
    def handle_add_course(self):
        course_id = self.course_id_entry.get().strip()
        course_name = self.course_name_entry.get().strip()
        instructor = self.instructor_entry.get().strip()
        max_students_str = self.max_students_entry.get().strip()
        if not course_id or not course_name or not instructor:
            messagebox.showerror("Error", "Please fill all course details")
            return
        try:
            max_students = int(max_students_str)
            if max_students <= 0:
                raise ValueError("Maximum students must be a positive number")
        except ValueError:
            messagebox.showerror("Error", "Maximum students must be a valid number")
            return
        success, message = self.system.add_course(course_id, course_name, instructor, max_students)
        if success:
            messagebox.showinfo("Course Added", message)
            self.course_id_entry.delete(0, tk.END)
            self.course_name_entry.delete(0, tk.END)
            self.instructor_entry.delete(0, tk.END)
            self.max_students_entry.delete(0, tk.END)
            self.max_students_entry.insert(0, "30")
            self.refresh_course_lists()
        else:
            messagebox.showerror("Error", message)
    
    def handle_logout(self):
        self.current_student = None
        self.student_info_label.config(text="Not logged in")
        self.notebook.tab(1, state="disabled")
        self.notebook.select(0)
        for item in self.available_courses_tree.get_children():
            self.available_courses_tree.delete(item)
        for item in self.enrolled_courses_tree.get_children():
            self.enrolled_courses_tree.delete(item)
        messagebox.showinfo("Logout", "You have been logged out successfully")

# main loop to run the app.
def main():
    root = tk.Tk()
    app = UniversityRegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
