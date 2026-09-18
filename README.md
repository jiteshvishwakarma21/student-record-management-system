# Student Record Management System

A menu-driven, console-based Python application for managing student records — built as **Assignment 1 (Mini Project)** for MCA Semester I – Python Programming.

## Project Description

This application allows a user to add, view, search, update, and delete student records through a simple text menu. All records are stored in a local JSON file (`records.json`), so data persists between program runs. The project was built to demonstrate core Python programming concepts in a single, cohesive, working application rather than in isolated snippets.

## Features

- **Add Student** – Enter a new student's ID, name, age, course, email, and marks, with input validation.
- **View All Students** – Display every stored record in a clear, labeled block format (Student ID, Name, Age, Course, Email, Marks) along with a total record count.
- **Search Student** – Search by exact Student ID or by partial/full name (case-insensitive).
- **Update Student** – Edit any field of an existing record; press Enter to keep the current value for any field.
- **Delete Student** – Remove a record after a confirmation prompt.
- **Persistent Storage** – Records are saved to `records.json` after every change, so nothing is lost when the program closes.
- **Input Validation & Error Handling** – Invalid menu choices, non-existent Student IDs, malformed email addresses, and file I/O errors are all handled gracefully without crashing the program.

## Technologies / Concepts Used

| Concept | Where it's used |
|---|---|
| Data types & variables | Records represented as dictionaries with `str`/`int` fields (Student ID, Name, Age, Course, Email, Marks) |
| Conditional statements | `if / elif / else` for menu routing and validation |
| Loops | `while True` for the main menu and input-retry loops; `for` for iterating/searching records |
| Functions | Every operation (add, view, search, update, delete, load, save, validate) is a separate function |
| Exception handling | `try / except` around file I/O, type conversions, and the main loop |
| File I/O | `json.load` / `json.dump` to persist records to `records.json` |
| Menu-driven design | A `display_menu()` function plus a dispatch loop in `main()` |

## Project Structure

```
record-management-app/
│
├── record_manager.py       # Main application source code
├── records.json             # Data file (auto-created/updated on each run)
├── README.md                # This file
└── docs/
    └── Assignment_Report.md # Full assignment documentation
```

## How to Run the Application

**Requirements:** Python 3.7 or higher (no external libraries needed — uses only the standard library).

1. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd record-management-app
   ```
2. Run the application:
   ```bash
   python3 record_manager.py
   ```
3. Follow the on-screen menu to add, view, search, update, or delete student records.
4. Records are automatically saved to `records.json` in the same folder. You can close and reopen the program at any time — your data will still be there.

## Sample Input / Output

```
=================================================
   STUDENT RECORD MANAGEMENT SYSTEM
=================================================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
=================================================
Enter your choice (1-6): 2

--- All Student Records ---
--------------------------------------------------
Student ID : S001
Name       : Jitesh Vishwakarma
Age        : 20
Course     : MCA
Email      : jitesh@example.com
Marks      : 85
--------------------------------------------------
Student ID : S002
Name       : Prajwal Bhosle
Age        : 21
Course     : MCA
Email      : prajwal@example.com
Marks      : 80
--------------------------------------------------
Student ID : S003
Name       : Keshav Sahu
Age        : 20
Course     : MCA
Email      : keshav@example.com
Marks      : 75
--------------------------------------------------
Total records: 3
```

Add screenshots of your own terminal session here (e.g., `screenshots/add_student.png`, `screenshots/view_students.png`) to demonstrate the working application, as required by the assignment.

## Error Handling Highlights

- Invalid menu choice → prompts the user again instead of crashing.
- Searching/updating/deleting a Student ID that doesn't exist → reported clearly, no crash.
- Invalid email format → rejected and re-prompted (on Add) or previous value kept (on Update).
- Missing or corrupted `records.json` → handled gracefully; the app starts with an empty record list instead of crashing.
- Any unexpected runtime error inside the menu loop is caught so the program never terminates unexpectedly.

## Author

- **Name:** Jitesh Vishwakarma
- **Roll No:** 10
- **Subject:** Python Programming
- **Faculty:** Rohan Sir
- **Course:** MCA Semester I
