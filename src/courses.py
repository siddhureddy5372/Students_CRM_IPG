from storage import load_data, save_data
from validations import is_unique, not_empty

FILE = "data/courses.json"
TEACHERS_FILE = "data/teachers.json"

def insert_course(disciplina):
    courses = load_data(FILE)

    if not is_unique(courses, "id", disciplina["id"]):
        print("❌ course ID exists")
        return

    if not not_empty(disciplina["name"]):
        print("❌ Name cannot be empty")
        return
    
    teachers = load_data(TEACHERS_FILE)
    teacher_exists = False
    for t in teachers:
        if t["id"] == disciplina["teacher_id"]:
            teacher_exists = True
            break
    if not teacher_exists:
        print("❌ Error: Teacher ID does not exist.")
        return

    courses.append(disciplina)
    save_data(FILE, courses)
    print("✅ course added")


def list_courses():
    courses = load_data(FILE)
    courses = sorted(courses, key=lambda t: t["id"])
    for t in courses:
        print(t)


def update_course(disciplina_id, new_data):
    courses = load_data(FILE)

    for t in courses:
        if t["id"] == disciplina_id:
            t.update(new_data)
            save_data(FILE, courses)
            print("✅ course updated")
            return

    print("❌ course not found")


def delete_course(disciplina_id):
    courses = load_data(FILE)
    new_disciplina = [t for t in courses if t["id"] != disciplina_id]

    if len(new_disciplina) == len(courses):
        print("❌ course not found")
        return

    save_data(FILE, new_disciplina)
    print("✅ course deleted")
