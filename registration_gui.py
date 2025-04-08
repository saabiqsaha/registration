import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from registration import Student, Course, EnrollmentSystem

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Registration System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.system = EnrollmentSystem()
        self.current_student = None
        
        # Dictionary to store course schedules
        self.course_schedules = {}
        self.load_course_schedules()
        
        self.setup_ui()
        
    def load_course_schedules(self):
        """Load course schedules from schedules.csv if it exists"""
        if os.path.exists("schedules.csv"):
            with open("schedules.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        course_id, day, time_slot = row[0], row[1], row[2]
                        if course_id not in self.course_schedules:
                            self.course_schedules[course_id] = []
                        self.course_schedules[course_id].append((day, time_slot))
        else:
            # Create default schedules for existing courses
            for course_id in self.system.courses:
                # Assign a random schedule (for demonstration)
                day = "Monday"  # Default day
                time_slot = "09:00-10:30"  # Default time
                self.course_schedules[course_id] = [(day, time_slot)]
            
            # Save the schedules
            self.save_course_schedules()
    
    def save_course_schedules(self):
        """Save course schedules to schedules.csv"""
        with open("schedules.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for course_id, schedules in self.course_schedules.items():
                for day, time_slot in schedules:
                    writer.writerow([course_id, day, time_slot])
    
    def has_schedule_conflict(self, course_id):
        """Check if enrolling in this course would create a schedule conflict"""
        if course_id not in self.course_schedules:
            return False
            
        # Get the schedule of the course to be added
        new_course_schedule = self.course_schedules[course_id]
        
        # Check against all currently enrolled courses
        for enrolled_course_id in self.current_student.registered_courses:
            if enrolled_course_id in self.course_schedules:
                enrolled_schedule = self.course_schedules[enrolled_course_id]
                
                # Check for conflicts
                for new_day, new_time in new_course_schedule:
                    for enrolled_day, enrolled_time in enrolled_schedule:
                        if new_day == enrolled_day and new_time == enrolled_time:
                            return True
        
        return False
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Login/Register frame
        self.auth_frame = ttk.LabelFrame(main_frame, text="Authentication", padding="10")
        self.auth_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.auth_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.student_id_entry = ttk.Entry(self.auth_frame, width=20)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.auth_frame, text="Login", command=self.login).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.auth_frame, text="Register", command=self.register_student).grid(row=0, column=3, padx=5, pady=5)
        
        # Course Management Frame
        self.course_frame = ttk.LabelFrame(main_frame, text="Course Management", padding="10")
        self.course_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Available Courses Frame
        available_frame = ttk.LabelFrame(self.course_frame, text="Available Courses")
        available_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create treeview for available courses
        self.available_tree = ttk.Treeview(available_frame, columns=("ID", "Name", "Instructor", "Enrollment", "Schedule"), show="headings")
        self.available_tree.heading("ID", text="Course ID")
        self.available_tree.heading("Name", text="Course Name")
        self.available_tree.heading("Instructor", text="Instructor")
        self.available_tree.heading("Enrollment", text="Enrollment")
        self.available_tree.heading("Schedule", text="Schedule")
        
        self.available_tree.column("ID", width=80)
        self.available_tree.column("Name", width=150)
        self.available_tree.column("Instructor", width=120)
        self.available_tree.column("Enrollment", width=100)
        self.available_tree.column("Schedule", width=150)
        
        self.available_tree.pack(fill=tk.BOTH, expand=True)
        
        available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.available_tree.yview)
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.available_tree.configure(yscrollcommand=available_scrollbar.set)
        
        # Registered Courses Frame
        registered_frame = ttk.LabelFrame(self.course_frame, text="My Registered Courses")
        registered_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create treeview for registered courses
        self.registered_tree = ttk.Treeview(registered_frame, columns=("ID", "Name", "Instructor", "Schedule"), show="headings")
        self.registered_tree.heading("ID", text="Course ID")
        self.registered_tree.heading("Name", text="Course Name")
        self.registered_tree.heading("Instructor", text="Instructor")
        self.registered_tree.heading("Schedule", text="Schedule")
        
        self.registered_tree.column("ID", width=80)
        self.registered_tree.column("Name", width=150)
        self.registered_tree.column("Instructor", width=120)
        self.registered_tree.column("Schedule", width=150)
        
        self.registered_tree.pack(fill=tk.BOTH, expand=True)
        
        registered_scrollbar = ttk.Scrollbar(registered_frame, orient=tk.VERTICAL, command=self.registered_tree.yview)
        registered_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.registered_tree.configure(yscrollcommand=registered_scrollbar.set)
        
        # Action Buttons Frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Enroll in Selected Course", command=self.enroll_in_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Drop Selected Course", command=self.drop_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh Course List", command=self.refresh_courses).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Add New Course", command=self.add_new_course).pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Please login or register to continue", anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Initialize with courses list
        self.refresh_courses()
        self.update_ui_for_auth_state()
    
    def update_ui_for_auth_state(self):
        """Update the UI based on whether a student is logged in or not"""
        if self.current_student:
            self.status_label.config(text=f"Logged in as: {self.current_student.name} (ID: {self.current_student.student_id})")
            self.refresh_registered_courses()
        else:
            self.status_label.config(text="Please login or register to continue")
            # Clear registered courses
            for item in self.registered_tree.get_children():
                self.registered_tree.delete(item)
    
    def login(self):
        student_id = self.student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
        
        if student_id in self.system.students:
            self.current_student = self.system.students[student_id]
            self.update_ui_for_auth_state()
            messagebox.showinfo("Success", f"Welcome back, {self.current_student.name}!")
        else:
            messagebox.showerror("Error", "Student not found. Please register first.")
    
    def register_student(self):
        student_id = self.student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
        
        if student_id in self.system.students:
            messagebox.showerror("Error", "Student ID already exists")
            return
        
        name = simpledialog.askstring("Register", "Enter your name:")
        if name:
            self.system.register_student(student_id, name)
            self.current_student = self.system.students[student_id]
            self.update_ui_for_auth_state()
    
    def add_new_course(self):
        """Add a new course to the system"""
        course_id = simpledialog.askstring("New Course", "Enter course ID:")
        if not course_id:
            return
            
        if course_id in self.system.courses:
            messagebox.showerror("Error", "Course ID already exists")
            return
            
        name = simpledialog.askstring("New Course", "Enter course name:")
        if not name:
            return
            
        instructor = simpledialog.askstring("New Course", "Enter instructor name:")
        if not instructor:
            return
            
        # Get schedule information
        day = simpledialog.askstring("New Course", "Enter day (e.g., Monday, Tuesday):")
        if not day:
            return
            
        time_slot = simpledialog.askstring("New Course", "Enter time slot (e.g., 09:00-10:30):")
        if not time_slot:
            return
            
        # Add the course
        self.system.add_course(course_id, name, instructor)
        
        # Save the schedule
        self.course_schedules[course_id] = [(day, time_slot)]
        self.save_course_schedules()
        
        # Refresh the courses list
        self.refresh_courses()
    
    def get_schedule_display(self, course_id):
        """Get a display string for the course schedule"""
        if course_id in self.course_schedules:
            schedules = []
            for day, time in self.course_schedules[course_id]:
                schedules.append(f"{day} {time}")
            return ", ".join(schedules)
        return "No schedule"
    
    def refresh_courses(self):
        # Clear the treeview
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        # Populate with courses
        for course_id, course in self.system.courses.items():
            enrollment = f"{len(course.enrolled_students)}/{course.max_students}"
            schedule = self.get_schedule_display(course_id)
            self.available_tree.insert("", tk.END, values=(course_id, course.name, course.instructor, enrollment, schedule))
    
    def refresh_registered_courses(self):
        if not self.current_student:
            return
            
        # Clear the treeview
        for item in self.registered_tree.get_children():
            self.registered_tree.delete(item)
        
        # Populate with registered courses
        for course_id in self.current_student.registered_courses:
            if course_id in self.system.courses:
                course = self.system.courses[course_id]
                schedule = self.get_schedule_display(course_id)
                self.registered_tree.insert("", tk.END, values=(course_id, course.name, course.instructor, schedule))
    
    def enroll_in_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected_item = self.available_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to enroll in")
            return
        
        course_id = self.available_tree.item(selected_item[0], "values")[0]
        
        # Check if the course is full
        course = self.system.courses[course_id]
        if len(course.enrolled_students) >= course.max_students:
            messagebox.showerror("Error", "Course is full")
            return
        
        # Check if already enrolled
        if course_id in self.current_student.registered_courses:
            messagebox.showerror("Error", "You are already enrolled in this course")
            return
        
        # Check for schedule conflicts
        if self.has_schedule_conflict(course_id):
            messagebox.showerror("Error", "Schedule conflict detected. Cannot enroll in this course.")
            return
        
        # Enroll the student
        self.system.enroll_student(self.current_student.student_id, course_id)
        self.refresh_courses()
        self.refresh_registered_courses()
    
    def drop_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected_item = self.registered_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to drop")
            return
        
        course_id = self.registered_tree.item(selected_item[0], "values")[0]
        
        # Drop the course
        self.system.drop_course(self.current_student.student_id, course_id)
        self.refresh_courses()
        self.refresh_registered_courses()

def main():
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 