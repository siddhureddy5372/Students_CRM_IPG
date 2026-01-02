from storage import load_data, save_data
from validations import is_unique, valid_email, valid_year, not_empty

FILE = "data/students.json"

def insert_student(student):
    students = load_data(FILE)

    if not is_unique(students, "id", student["id"]):
        print("❌ Student ID already exists")
        return

    if not valid_email(student["email"]):
        print("❌ Invalid email")
        return

    if not valid_year(student["year"]):
        print("❌ Invalid year")
        return

    students.append(student)
    save_data(FILE, students)
    print("✅ Student added successfully")

def list_students():
    students = load_data(FILE)
    print(f"{'ID':<10} {'Name':<20} {'Course':<10}")
    print("-" * 40)
    for s in students:
        print(f"{s['id']:<10} {s['name']:<20} {s['course']:<10}")

def search_student_by_name(name):
    students = load_data(FILE)
    print(f"{'ID':<10} {'Name':<20} {'Course':<10}")
    print("-" * 40)
    for s in students:
        if name.lower() in s["name"].lower():
            print(f"{s['id']:<10} {s['name']:<20} {s['course']:<10}")

def update_student(student_id, new_data):
    students = load_data(FILE)

    for s in students:
        if s["id"] == student_id:
            if "email" in new_data and not valid_email(new_data["email"]):
                print("❌ Invalid email")
                return

            if "year" in new_data and not valid_year(new_data["year"]):
                print("❌ Invalid year")
                return

            s.update(new_data)
            save_data(FILE, students)
            print("✅ Student updated")
            return

    print("❌ Student not found")


def delete_student(student_id):
    students = load_data(FILE)
    new_students = [s for s in students if s["id"] != student_id]

    if len(new_students) == len(students):
        print("❌ Student not found")
        return

    save_data(FILE, new_students)
    print("✅ Student deleted")
