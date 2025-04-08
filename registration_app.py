import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from enrollment_system import EnrollmentSystem

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Registration System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.system = EnrollmentSystem()
        self.current_student = None

        # Set up the notebook for different screens
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for different screens
        self.login_frame = ttk.Frame(self.notebook, padding=20)
        self.courses_frame = ttk.Frame(self.notebook, padding=20)
        
        # Add frames to notebook
        self.notebook.add(self.login_frame, text="Login/Register")
        self.notebook.add(self.courses_frame, text="Courses")
        
        # Set up login screen
        self.setup_login_screen()
        
        # Set up courses screen
        self.setup_courses_screen()
        
        # Disable courses tab until login
        self.notebook.tab(1, state="disabled")
        
        # Status bar at the bottom
        self.status_var = tk.StringVar(value="Welcome to the University Course Registration System")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_login_screen(self):
        # Title
        title_label = ttk.Label(self.login_frame, text="Student Authentication", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Login form
        login_frame = ttk.LabelFrame(self.login_frame, text="Login or Register", padding=20)
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student ID
        ttk.Label(login_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.student_id_var = tk.StringVar()
        self.student_id_entry = ttk.Entry(login_frame, textvariable=self.student_id_var, width=30)
        self.student_id_entry.grid(row=0, column=1, pady=10, padx=5)
        self.student_id_entry.focus()
        
        # Student Name (for registration)
        ttk.Label(login_frame, text="Student Name:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.student_name_var = tk.StringVar()
        self.student_name_entry = ttk.Entry(login_frame, textvariable=self.student_name_var, width=30)
        self.student_name_entry.grid(row=1, column=1, pady=10, padx=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(login_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Login button
        login_btn = ttk.Button(btn_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        # Register button
        register_btn = ttk.Button(btn_frame, text="Register", command=self.register)
        register_btn.pack(side=tk.LEFT, padx=10)
        
        # Information text
        info_text = ("Please enter your Student ID to login.\n"
                     "If you're a new student, enter your ID and name, then click Register.")
        info_label = ttk.Label(login_frame, text=info_text, foreground="gray")
        info_label.grid(row=3, column=0, columnspan=2, pady=20)
        
    def setup_courses_screen(self):
        # Title with student info
        self.student_info_var = tk.StringVar(value="Student: Not logged in")
        student_info_label = ttk.Label(self.courses_frame, textvariable=self.student_info_var, font=("Arial", 12, "bold"))
        student_info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Split into two panes
        paned_window = ttk.PanedWindow(self.courses_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Available courses frame
        available_frame = ttk.LabelFrame(paned_window, text="Available Courses")
        
        # My courses frame
        my_courses_frame = ttk.LabelFrame(paned_window, text="My Enrolled Courses")
        
        paned_window.add(available_frame, weight=1)
        paned_window.add(my_courses_frame, weight=1)
        
        # Available courses treeview
        columns = ("id", "name", "instructor", "enrollment")
        self.available_tree = ttk.Treeview(available_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        self.available_tree.heading("id", text="ID")
        self.available_tree.heading("name", text="Course Name")
        self.available_tree.heading("instructor", text="Instructor")
        self.available_tree.heading("enrollment", text="Enrollment")
        
        # Define columns
        self.available_tree.column("id", width=80)
        self.available_tree.column("name", width=200)
        self.available_tree.column("instructor", width=150)
        self.available_tree.column("enrollment", width=100)
        
        # Add scrollbar to available courses
        scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.available_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # My courses treeview
        my_columns = ("id", "name", "instructor")
        self.my_courses_tree = ttk.Treeview(my_courses_frame, columns=my_columns, show="headings", selectmode="browse")
        
        # Define headings
        self.my_courses_tree.heading("id", text="ID")
        self.my_courses_tree.heading("name", text="Course Name")
        self.my_courses_tree.heading("instructor", text="Instructor")
        
        # Define columns
        self.my_courses_tree.column("id", width=80)
        self.my_courses_tree.column("name", width=200)
        self.my_courses_tree.column("instructor", width=150)
        
        # Add scrollbar to my courses
        my_scrollbar = ttk.Scrollbar(my_courses_frame, orient=tk.VERTICAL, command=self.my_courses_tree.yview)
        self.my_courses_tree.configure(yscrollcommand=my_scrollbar.set)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(self.courses_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Enroll button
        self.enroll_btn = ttk.Button(button_frame, text="Enroll in Selected Course", command=self.enroll_student)
        self.enroll_btn.pack(side=tk.LEFT, padx=5)
        
        # Drop button
        self.drop_btn = ttk.Button(button_frame, text="Drop Selected Course", command=self.drop_course)
        self.drop_btn.pack(side=tk.LEFT, padx=5)
        
        # Add course button
        self.add_course_btn = ttk.Button(button_frame, text="Add New Course", command=self.add_course)
        self.add_course_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        self.refresh_btn = ttk.Button(button_frame, text="Refresh Courses", command=self.refresh_courses)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Logout button
        self.logout_btn = ttk.Button(button_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(side=tk.RIGHT, padx=5)
    
    def login(self):
        student_id = self.student_id_var.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
        
        if student_id in self.system.students:
            self.current_student = self.system.students[student_id]
            self.student_info_var.set(f"Student: {self.current_student.name} (ID: {self.current_student.student_id})")
            self.status_var.set(f"Logged in as {self.current_student.name}")
            
            # Enable courses tab and switch to it
            self.notebook.tab(1, state="normal")
            self.notebook.select(1)
            
            # Refresh course lists
            self.refresh_courses()
            messagebox.showinfo("Success", f"Welcome back, {self.current_student.name}!")
        else:
            messagebox.showerror("Error", "Student not found. Please register first.")
    
    def register(self):
        student_id = self.student_id_var.get().strip()
        student_name = self.student_name_var.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
            
        if not student_name:
            messagebox.showerror("Error", "Please enter a student name")
            return
        
        success, message = self.system.register_student(student_id, student_name)
        if success:
            self.current_student = self.system.students[student_id]
            self.student_info_var.set(f"Student: {self.current_student.name} (ID: {self.current_student.student_id})")
            self.status_var.set(f"Registered and logged in as {self.current_student.name}")
            
            # Enable courses tab and switch to it
            self.notebook.tab(1, state="normal")
            self.notebook.select(1)
            
            # Refresh course lists
            self.refresh_courses()
            messagebox.showinfo("Success", "Registration successful! You are now logged in.")
            
            # Guide user to add a course if none exist
            if not self.system.courses:
                self.prompt_add_course()
        else:
            messagebox.showerror("Error", message)
    
    def prompt_add_course(self):
        """Prompt user to add a course if none exist"""
        response = messagebox.askyesno("Add Course", "Would you like to add a new course to the system?")
        if response:
            self.add_course()
    
    def refresh_courses(self):
        """Refresh both available courses and my courses lists"""
        # Clear previous data
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
            
        for item in self.my_courses_tree.get_children():
            self.my_courses_tree.delete(item)
        
        # Load available courses
        available_courses = self.system.get_available_courses()
        for course in available_courses:
            self.available_tree.insert("", "end", values=(
                course['id'], 
                course['name'], 
                course['instructor'], 
                course['enrollment']
            ))
        
        # Load enrolled courses if student is logged in
        if self.current_student:
            enrolled_courses = self.system.get_student_courses(self.current_student.student_id)
            for course in enrolled_courses:
                self.my_courses_tree.insert("", "end", values=(
                    course['id'],
                    course['name'],
                    course['instructor']
                ))
        
        self.status_var.set("Course lists refreshed")
    
    def enroll_student(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected_item = self.available_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to enroll in")
            return
        
        # Get course ID from the selected item
        course_id = self.available_tree.item(selected_item, "values")[0]
        
        # Try to enroll
        success, message = self.system.enroll_student(self.current_student.student_id, course_id)
        if success:
            self.refresh_courses()
            messagebox.showinfo("Success", message)
            self.status_var.set(f"Enrolled in course {course_id}")
        else:
            messagebox.showerror("Error", message)
    
    def drop_course(self):
        if not self.current_student:
            messagebox.showerror("Error", "Please login first")
            return
        
        selected_item = self.my_courses_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course to drop")
            return
        
        # Get course ID from the selected item
        course_id = self.my_courses_tree.item(selected_item, "values")[0]
        
        # Confirm before dropping
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to drop course {course_id}?")
        if not confirm:
            return
        
        # Try to drop the course
        success, message = self.system.drop_course(self.current_student.student_id, course_id)
        if success:
            self.refresh_courses()
            messagebox.showinfo("Success", message)
            self.status_var.set(f"Dropped course {course_id}")
        else:
            messagebox.showerror("Error", message)
    
    def add_course(self):
        # Create a dialog to get course information
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Course")
        add_window.geometry("400x300")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Course form
        course_frame = ttk.Frame(add_window, padding=20)
        course_frame.pack(fill=tk.BOTH, expand=True)
        
        # Course ID
        ttk.Label(course_frame, text="Course ID:").grid(row=0, column=0, sticky=tk.W, pady=10)
        course_id_var = tk.StringVar()
        course_id_entry = ttk.Entry(course_frame, textvariable=course_id_var, width=30)
        course_id_entry.grid(row=0, column=1, pady=10, padx=5)
        course_id_entry.focus()
        
        # Course Name
        ttk.Label(course_frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=10)
        course_name_var = tk.StringVar()
        course_name_entry = ttk.Entry(course_frame, textvariable=course_name_var, width=30)
        course_name_entry.grid(row=1, column=1, pady=10, padx=5)
        
        # Instructor
        ttk.Label(course_frame, text="Instructor:").grid(row=2, column=0, sticky=tk.W, pady=10)
        instructor_var = tk.StringVar()
        instructor_entry = ttk.Entry(course_frame, textvariable=instructor_var, width=30)
        instructor_entry.grid(row=2, column=1, pady=10, padx=5)
        
        # Button frame
        btn_frame = ttk.Frame(course_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Function to add the course and close dialog
        def add_course_action():
            course_id = course_id_var.get().strip()
            course_name = course_name_var.get().strip()
            instructor = instructor_var.get().strip()
            
            if not course_id or not course_name or not instructor:
                messagebox.showerror("Error", "All fields are required", parent=add_window)
                return
            
            success, message = self.system.add_course(course_id, course_name, instructor)
            if success:
                self.refresh_courses()
                messagebox.showinfo("Success", message, parent=add_window)
                add_window.destroy()
                
                # Prompt to enroll in the new course
                if self.current_student:
                    self.prompt_enroll_new_course(course_id)
            else:
                messagebox.showerror("Error", message, parent=add_window)
        
        # Add and Cancel buttons
        add_btn = ttk.Button(btn_frame, text="Add Course", command=add_course_action)
        add_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=add_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def prompt_enroll_new_course(self, course_id):
        """Ask if the user wants to enroll in the course they just created"""
        if course_id in self.system.courses:
            course = self.system.courses[course_id]
            response = messagebox.askyesno(
                "Enroll in Course", 
                f"Would you like to enroll in the course you just added?\n\n{course_id}: {course.name}"
            )
            if response:
                success, message = self.system.enroll_student(self.current_student.student_id, course_id)
                if success:
                    self.refresh_courses()
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
    
    def logout(self):
        self.current_student = None
        self.student_info_var.set("Student: Not logged in")
        self.status_var.set("Logged out successfully")
        
        # Clear course lists
        for item in self.my_courses_tree.get_children():
            self.my_courses_tree.delete(item)
        
        # Disable courses tab and go back to login
        self.notebook.tab(1, state="disabled")
        self.notebook.select(0)
        
        # Clear login fields
        self.student_id_var.set("")
        self.student_name_var.set("")
        self.student_id_entry.focus()
        
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")

def main():
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 