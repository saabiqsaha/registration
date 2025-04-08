# University Course Registration System

A simple college course registration system implemented using Python and Tkinter, following object-oriented programming principles.

## Features

- Student registration and login
- View available courses with enrollment information
- Enroll in courses (with capacity checks)
- Drop courses
- Add new courses to the system
- Data persistence using CSV files

## System Requirements

- Python 3.6 or higher
- Tkinter (included with most Python installations)

## Project Structure

The application is organized into three main files:

1. `student.py` - Contains the Student class definition
2. `course.py` - Contains the Course class definition
3. `enrollment_system.py` - Core functionality for managing students and courses
4. `registration_app.py` - The Tkinter GUI interface

## Data Storage

The system uses three CSV files to store data:

- `students.csv` - Stores student information
- `courses.csv` - Stores course details
- `enrollments.csv` - Records enrollment relationships

## How to Run

1. Make sure you have Python installed
2. Run the application using:

```
python registration_app.py
```

## Using the Application

### Registration/Login Flow

1. Enter your student ID and name
2. Click "Register" to create a new account
3. Once registered, you'll automatically be logged in and taken to the courses screen
4. If no courses exist, you'll be prompted to add a new course

### Course Management

1. View available courses in the left panel
2. View your enrolled courses in the right panel
3. Select a course from the available courses and click "Enroll" to register
4. Select one of your enrolled courses and click "Drop" to unenroll
5. Click "Add New Course" to create a new course (you'll be prompted to enroll after creating)

## Implementation

The system implements the following requirements:

- ✅ Student registration
- ✅ Course viewing
- ✅ Course enrollment with capacity limits (30 students per course)
- ✅ Course dropping
- ✅ CSV-based storage
- ✅ Error handling for invalid inputs
- ✅ User-friendly interface with guided workflow 