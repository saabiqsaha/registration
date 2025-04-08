import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# --------- Student Class ---------
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.registered_courses = set()

# --------- Course Class ---------
class Course:
    def __init__(self, course_id, name, instructor, max_students=30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students

# --------- Registration System ---------
class RegistrationSystem:
    def __init__(self, root):
        # Initialize the data
        self.students = {}
        self.courses = {}
        self.current_student = None
        
        # Load data from CSV files
        self.load_data()
        
        # Set up the UI
        self.root = root
        self.root.title("Course Registration System")
        self.root.geometry("800x500")
        
        # Main frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create frames
        self.login_frame = ttk.LabelFrame(main_frame, text="Login/Register", padding=10)
        self.login_frame.pack(fill=tk.X, pady=5)
        
        self.course_frame = ttk.LabelFrame(main_frame, text="Course Management", padding=10)
        self.course_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Please login or register")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Setup login UI
        self.setup_login_ui()
        
        # Setup course management UI
        self.setup_course_ui()
        
        # Update UI based on login state
        self.update_ui_state()
    
    def load_data(self):
        # Load student data
        if os.path.exists("students.csv"):
            with open("students.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        student_id, name, *courses = row
                        student = Student(student_id, name)
                        student.registered_courses = set(courses)
                        self.students[student_id] = student
        
        # Load course data
        if os.path.exists("courses.csv"):
            with open("courses.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        course_id, name, instructor, *students = row
                        course = Course(course_id, name, instructor)
                        course.enrolled_students = set(students)
                        self.courses[course_id] = course
    
    def save_data(self):
        # Save student data
        with open("students.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                writer.writerow([student.student_id, student.name] + list(student.registered_courses))
        
        # Save course data
        with open("courses.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor] + list(course.enrolled_students))
        
        # Save enrollments data
        with open("enrollments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                for course_id in student.registered_courses:
                    writer.writerow([student.student_id, course_id])
    
    def setup_login_ui(self):
        # Student ID
        ttk.Label(self.login_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.student_id_var = tk.StringVar()
        self.student_id_entry = ttk.Entry(self.login_frame, textvariable=self.student_id_var, width=20)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Student Name
        ttk.Label(self.login_frame, text="Student Name:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.student_name_var = tk.StringVar()
        self.student_name_entry = ttk.Entry(self.login_frame, textvariable=self.student_name_var, width=20)
        self.student_name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Login/Register buttons
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(self.login_frame, text="Register", command=self.register).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(self.login_frame, text="Logout", command=self.logout).grid(row=0, column=6, padx=5, pady=5)
    
    def setup_course_ui(self):
        # Split course frame into two parts
        left_frame = ttk.Frame(self.course_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(self.course_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Available Courses section
        ttk.Label(left_frame, text="Available Courses").pack(anchor=tk.W)
        
        # Course list with scrollbar
        columns = ("id", "name", "instructor", "enrollment")
        self.course_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=10)
        
        self.course_tree.heading("id", text="ID")
        self.course_tree.heading("name", text="Course Name")
        self.course_tree.heading("instructor", text="Instructor")
        self.course_tree.heading("enrollment", text="Enrollment")
        
        self.course_tree.column("id", width=50)
        self.course_tree.column("name", width=150)
        self.course_tree.column("instructor", width=100)
        self.course_tree.column("enrollment", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # My Courses section
        ttk.Label(right_frame, text="My Registered Courses").pack(anchor=tk.W)
        
        # My course list with scrollbar
        my_columns = ("id", "name", "instructor")
        self.my_course_tree = ttk.Treeview(right_frame, columns=my_columns, show="headings", height=10)
        
        self.my_course_tree.heading("id", text="ID")
        self.my_course_tree.heading("name", text="Course Name")
        self.my_course_tree.heading("instructor", text="Instructor")
        
        self.my_course_tree.column("id", width=50)
        self.my_course_tree.column("name", width=150)
        self.my_course_tree.column("instructor", width=100)
        
        # Add scrollbar
        my_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.my_course_tree.yview)
        self.my_course_tree.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(self.course_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Action buttons
        ttk.Button(button_frame, text="Add Course", command=self.add_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Enroll", command=self.enroll_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Drop Course", command=self.drop_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_courses).pack(side=tk.LEFT, padx=5)
    
    def update_ui_state(self):
        # Update UI based on login state
        if self.current_student:
            self.status_var.set(f"Logged in as: {self.current_student.name} (ID: {self.current_student.student_id})")
            self.refresh_courses()
        else:
            self.status_var.set("Please login or register")
            # Clear course trees
            for item in self.course_tree.get_children():
                self.course_tree.delete(item)
            for item in self.my_course_tree.get_children():
                self.my_course_tree.delete(item)
    
    def login(self):
        student_id = self.student_id_var.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
        
        if student_id in self.students:
            self.current_student = self.students[student_id]
            self.update_ui_state()
            messagebox.showinfo("Success", f"Welcome back, {self.current_student.name}!")
            
            # If no courses exist, prompt to add one
            if not self.courses:
                self.prompt_add_course()
        else:
            messagebox.showerror("Error", "Student not found. Please register first.")
    
    def register(self):
        student_id = self.student_id_var.get().strip()
        name = self.student_name_var.get().strip()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Please enter both student ID and name")
            return
        
        if student_id in self.students:
            messagebox.showerror("Error", "Student ID already exists")
            return
        
        # Register new student
        self.students[student_id] = Student(student_id, name)
        self.current_student = self.students[student_id]
        self.save_data()
        
        self.update_ui_state()
        messagebox.showinfo("Success", "Registration successful!")
        
        # If no courses exist, prompt to add one
        if not self.courses:
            self.prompt_add_course()
    
    def logout(self):
        self.current_student = None
        self.student_id_var.set("")
        self.student_name_var.set("")
        self.update_ui_state()
        messagebox.showinfo("Logout", "You have been logged out.")
    
    def prompt_add_course(self):
        response = messagebox.askyesno("Add Course", "No courses are available. Would you like to add a new course?")
        if response:
            self.add_course()
    
    def add_course(self):
        # Open a dialog to add course details
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Course")
        add_window.geometry("300x200")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Course form
        frame = ttk.Frame(add_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Course ID
        ttk.Label(frame, text="Course ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_id_var = tk.StringVar()
        course_id_entry = ttk.Entry(frame, textvariable=course_id_var)
        course_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Course Name
        ttk.Label(frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        course_name_var = tk.StringVar()
        course_name_entry = ttk.Entry(frame, textvariable=course_name_var)
        course_name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Instructor
        ttk.Label(frame, text="Instructor:").grid(row=2, column=0, sticky=tk.W, pady=5)
        instructor_var = tk.StringVar()
        instructor_entry = ttk.Entry(frame, textvariable=instructor_var)
        instructor_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Add button function
        def save_course():
            course_id = course_id_var.get().strip()
            name = course_name_var.get().strip()
            instructor = instructor_var.get().strip()
            
            if not course_id or not name or not instructor:
                messagebox.showerror("Error", "All fields are required", parent=add_window)
                return
            
            if course_id in self.courses:
                messagebox.showerror("Error", "Course ID already exists", parent=add_window)
                return
            
            # Add the course
            self.courses[course_id] = Course(course_id, name, instructor)
            self.save_data()
            self.refresh_courses()
            
            add_window.destroy()
            messagebox.showinfo("Success", "Course added successfully")
            
            # Prompt to enroll in the new course
            if self.current_student:
                self.prompt_enroll(course_id)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Course", command=save_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=add_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def prompt_enroll(self, course_id):
        if course_id in self.courses:
            course = self.courses[course_id]
            response = messagebox.askyesno(
                "Enroll",
                f"Would you like to enroll in {course_id}: {course.name}?"
            )
            if response:
                self.enroll_in_course(course_id)
    
    def enroll_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a course to enroll in")
            return
        
        course_id = self.course_tree.item(selected[0], "values")[0]
        self.enroll_in_course(course_id)
    
    def enroll_in_course(self, course_id):
        if course_id not in self.courses or not self.current_student:
            return
        
        course = self.courses[course_id]
        
        # Check if course is full
        if len(course.enrolled_students) >= course.max_students:
            messagebox.showerror("Error", "Course is full")
            return
        
        # Check if already enrolled
        if course_id in self.current_student.registered_courses:
            messagebox.showerror("Error", "You are already enrolled in this course")
            return
        
        # Enroll the student
        self.current_student.registered_courses.add(course_id)
        course.enrolled_students.add(self.current_student.student_id)
        self.save_data()
        self.refresh_courses()
        
        messagebox.showinfo("Success", f"Successfully enrolled in {course.name}")
    
    def drop_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected = self.my_course_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a course to drop")
            return
        
        course_id = self.my_course_tree.item(selected[0], "values")[0]
        
        # Confirm drop
        course = self.courses[course_id]
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to drop {course.name}?")
        if not confirm:
            return
        
        # Drop the course
        self.current_student.registered_courses.remove(course_id)
        course.enrolled_students.discard(self.current_student.student_id)
        self.save_data()
        self.refresh_courses()
        
        messagebox.showinfo("Success", f"Successfully dropped {course.name}")
    
    def refresh_courses(self):
        # Clear tree views
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        for item in self.my_course_tree.get_children():
            self.my_course_tree.delete(item)
        
        # Update available courses
        for course_id, course in self.courses.items():
            enrollment = f"{len(course.enrolled_students)}/{course.max_students}"
            self.course_tree.insert("", "end", values=(
                course_id, course.name, course.instructor, enrollment
            ))
        
        # Update my courses if logged in
        if self.current_student:
            for course_id in self.current_student.registered_courses:
                if course_id in self.courses:
                    course = self.courses[course_id]
                    self.my_course_tree.insert("", "end", values=(
                        course_id, course.name, course.instructor
                    ))

# --------- Start the Application ---------
def main():
    root = tk.Tk()
    app = RegistrationSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main() 