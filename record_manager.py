"""
Console Record-Management Application
--------------------------------------
Author: <Your Name Here>
Course: MCA Semester I - Python Programming & Relational Database

Description:
A menu-driven console application to manage student records.
Supports Add, View, Search, Update, and Delete operations.
Records are persisted to a local JSON file so data survives
between program runs.

Python concepts demonstrated:
    - Data types & variables (str, int, dict, list)
    - Conditional statements & loops (if/elif/else, while, for)
    - Functions (modular design, one function per responsibility)
    - Exception handling (try/except/else/finally)
    - File I/O (JSON read/write with error handling)
    - Menu-driven console application design
"""

import json
import os
import re

# ---------------------------------------------------------------------------
# Constants / Global configuration
# ---------------------------------------------------------------------------
DATA_FILE = "records.json"


# ---------------------------------------------------------------------------
# File I/O functions
# ---------------------------------------------------------------------------
def load_records():
    """
    Load records from the JSON data file.

    Returns:
        list[dict]: A list of record dictionaries. Returns an empty list
        if the file does not exist, is empty, or contains invalid JSON.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print("Warning: Data file is corrupted. Starting with an empty record list.")
        return []
    except (IOError, OSError) as error:
        print(f"Error reading data file: {error}")
        return []


def save_records(records):
    """
    Save the list of records to the JSON data file.

    Args:
        records (list[dict]): The list of records to persist.

    Returns:
        bool: True if the save succeeded, False otherwise.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
        return True
    except (IOError, OSError) as error:
        print(f"Error saving data file: {error}")
        return False


# ---------------------------------------------------------------------------
# Validation helper functions
# ---------------------------------------------------------------------------
def get_next_id(records):
    """Generate the next unique numeric ID based on existing records."""
    if not records:
        return 1
    return max(record["id"] for record in records) + 1


def is_valid_email(email):
    """Basic email format validation using a regular expression."""
    pattern = r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate that a phone number contains 10 digits."""
    return phone.isdigit() and len(phone) == 10


def get_non_empty_input(prompt):
    """Repeatedly prompt the user until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_valid_email_input(prompt):
    """Repeatedly prompt the user until a valid email address is entered."""
    while True:
        email = input(prompt).strip()
        if is_valid_email(email):
            return email
        print("Invalid email format. Example: name@example.com")


def get_valid_phone_input(prompt):
    """Repeatedly prompt the user until a valid 10-digit phone number is entered."""
    while True:
        phone = input(prompt).strip()
        if is_valid_phone(phone):
            return phone
        print("Invalid phone number. Please enter exactly 10 digits.")


def get_valid_semester_input(prompt):
    """Repeatedly prompt the user until a valid semester number (1-6) is entered."""
    while True:
        value = input(prompt).strip()
        try:
            semester = int(value)
            if 1 <= semester <= 6:
                return semester
            print("Semester must be a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a whole number for semester.")


# ---------------------------------------------------------------------------
# Core record-management functions (CRUD)
# ---------------------------------------------------------------------------
def add_record(records):
    """Add a new student record after collecting validated input."""
    print("\n--- Add New Record ---")
    name = get_non_empty_input("Enter student name: ")
    course = get_non_empty_input("Enter course name (e.g., MCA): ")
    semester = get_valid_semester_input("Enter semester (1-6): ")
    email = get_valid_email_input("Enter email address: ")
    phone = get_valid_phone_input("Enter 10-digit phone number: ")

    new_record = {
        "id": get_next_id(records),
        "name": name,
        "course": course,
        "semester": semester,
        "email": email,
        "phone": phone,
    }

    records.append(new_record)

    if save_records(records):
        print(f"Record added successfully with ID: {new_record['id']}")
    else:
        print("Record was added in memory but could not be saved to disk.")


def view_records(records):
    """Display all student records in a formatted table."""
    print("\n--- All Records ---")
    if not records:
        print("No records found.")
        return

    header = f"{'ID':<5}{'Name':<20}{'Course':<12}{'Sem':<5}{'Email':<28}{'Phone':<12}"
    print(header)
    print("-" * len(header))
    for record in records:
        print(
            f"{record['id']:<5}{record['name']:<20}{record['course']:<12}"
            f"{record['semester']:<5}{record['email']:<28}{record['phone']:<12}"
        )


def find_record_by_id(records, record_id):
    """Return the record dict matching record_id, or None if not found."""
    for record in records:
        if record["id"] == record_id:
            return record
    return None


def search_record(records):
    """Search records by ID or by name (case-insensitive, partial match)."""
    print("\n--- Search Record ---")
    print("1. Search by ID")
    print("2. Search by Name")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        try:
            record_id = int(input("Enter record ID: ").strip())
        except ValueError:
            print("Invalid ID. Please enter a numeric value.")
            return

        record = find_record_by_id(records, record_id)
        if record:
            print("\nRecord found:")
            print(record)
        else:
            print("No record found with that ID.")

    elif choice == "2":
        name_query = input("Enter name (or part of it) to search: ").strip().lower()
        matches = [r for r in records if name_query in r["name"].lower()]

        if matches:
            print(f"\n{len(matches)} matching record(s) found:")
            for record in matches:
                print(record)
        else:
            print("No matching records found.")

    else:
        print("Invalid choice. Returning to main menu.")


def update_record(records):
    """Update an existing record's fields, keeping current values if left blank."""
    print("\n--- Update Record ---")
    try:
        record_id = int(input("Enter the ID of the record to update: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    record = find_record_by_id(records, record_id)
    if not record:
        print("No record found with that ID.")
        return

    print("Leave a field blank to keep its current value.")

    new_name = input(f"Name [{record['name']}]: ").strip()
    new_course = input(f"Course [{record['course']}]: ").strip()
    new_semester = input(f"Semester [{record['semester']}]: ").strip()
    new_email = input(f"Email [{record['email']}]: ").strip()
    new_phone = input(f"Phone [{record['phone']}]: ").strip()

    if new_name:
        record["name"] = new_name
    if new_course:
        record["course"] = new_course
    if new_semester:
        try:
            semester_val = int(new_semester)
            if 1 <= semester_val <= 6:
                record["semester"] = semester_val
            else:
                print("Semester out of range (1-6). Keeping previous value.")
        except ValueError:
            print("Invalid semester value. Keeping previous value.")
    if new_email:
        if is_valid_email(new_email):
            record["email"] = new_email
        else:
            print("Invalid email format. Keeping previous value.")
    if new_phone:
        if is_valid_phone(new_phone):
            record["phone"] = new_phone
        else:
            print("Invalid phone format. Keeping previous value.")

    if save_records(records):
        print("Record updated successfully.")
    else:
        print("Record was updated in memory but could not be saved to disk.")


def delete_record(records):
    """Delete a record after user confirmation."""
    print("\n--- Delete Record ---")
    try:
        record_id = int(input("Enter the ID of the record to delete: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    record = find_record_by_id(records, record_id)
    if not record:
        print("No record found with that ID.")
        return

    confirm = input(
        f"Are you sure you want to delete '{record['name']}' (ID: {record_id})? (y/n): "
    ).strip().lower()

    if confirm == "y":
        records.remove(record)
        if save_records(records):
            print("Record deleted successfully.")
        else:
            print("Record was deleted in memory but could not be saved to disk.")
    else:
        print("Delete cancelled.")


# ---------------------------------------------------------------------------
# Menu / Application driver
# ---------------------------------------------------------------------------
def display_menu():
    """Print the main menu options."""
    print("\n" + "=" * 45)
    print("   STUDENT RECORD MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add Record")
    print("2. View All Records")
    print("3. Search Record")
    print("4. Update Record")
    print("5. Delete Record")
    print("6. Exit")
    print("=" * 45)


def main():
    """Main application loop: load data, show menu, dispatch actions."""
    records = load_records()
    print("Welcome to the Student Record Management System!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                add_record(records)
            elif choice == "2":
                view_records(records)
            elif choice == "3":
                search_record(records)
            elif choice == "4":
                update_record(records)
            elif choice == "5":
                delete_record(records)
            elif choice == "6":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\nOperation interrupted by user. Returning to main menu.")
        except Exception as error:
            # Catch-all safety net so unexpected runtime errors never crash the app.
            print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
