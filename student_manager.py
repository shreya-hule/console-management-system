"""Student Record Manager: a small, JSON-backed console assignment."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read student data; starting with an empty list.")
        return []


def save_students(students):
    DATA_FILE.write_text(json.dumps(students, indent=2), encoding="utf-8")


def ask_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def ask_marks(prompt="Marks (0-100): "):
    while True:
        try:
            marks = float(input(prompt))
            if 0 <= marks <= 100:
                return marks
        except ValueError:
            pass
        print("Enter a number from 0 to 100.")


def next_id(students):
    return max((student["id"] for student in students), default=0) + 1


def add_student(students):
    student = {
        "id": next_id(students),
        "name": ask_nonempty("Student name: "),
        "course": ask_nonempty("Course: "),
        "marks": ask_marks(),
    }
    students.append(student)
    save_students(students)
    print(f"Added {student['name']} with ID {student['id']}.")


def list_students(students):
    if not students:
        print("No student records yet.")
        return
    print("\nID   NAME                     COURSE               MARKS")
    print("-" * 62)
    for s in students:
        print(f"{s['id']:<4} {s['name'][:24]:<24} {s['course'][:20]:<20} {s['marks']:>5.1f}")


def find_student(students, student_id):
    return next((s for s in students if s["id"] == student_id), None)


def update_student(students):
    try:
        student_id = int(input("Student ID to update: "))
    except ValueError:
        print("ID must be a number.")
        return
    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return
    print("Press Enter to keep the current value.")
    name = input(f"Name [{student['name']}]: ").strip()
    course = input(f"Course [{student['course']}]: ").strip()
    marks = input(f"Marks [{student['marks']}]: ").strip()
    if name:
        student["name"] = name
    if course:
        student["course"] = course
    if marks:
        try:
            value = float(marks)
            if not 0 <= value <= 100:
                raise ValueError
            student["marks"] = value
        except ValueError:
            print("Invalid marks; the previous mark was kept.")
    save_students(students)
    print("Student record updated.")


def delete_student(students):
    try:
        student_id = int(input("Student ID to delete: "))
    except ValueError:
        print("ID must be a number.")
        return
    student = find_student(students, student_id)
    if not student:
        print("Student not found.")
        return
    students.remove(student)
    save_students(students)
    print(f"Deleted {student['name']}.")


def search_students(students):
    term = input("Search name or course: ").strip().casefold()
    results = [s for s in students if term in s["name"].casefold() or term in s["course"].casefold()]
    if results:
        list_students(results)
    else:
        print("No matching students found.")


def main():
    students = load_students()
    actions = {"1": lambda: add_student(students), "2": lambda: list_students(students),
               "3": lambda: search_students(students), "4": lambda: update_student(students),
               "5": lambda: delete_student(students)}
    while True:
        print("\nSTUDENT RECORD MANAGER")
        print("1. Add student   2. List students   3. Search students")
        print("4. Update student   5. Delete student   0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Choose a menu option from 0 to 5.")


if __name__ == "__main__":
    main()
