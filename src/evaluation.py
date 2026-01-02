from storage import load_data, save_data
from validations import is_unique

FILE = "data/evaluation.json"
STUDENT_FILE = "data/students.json"
COURSE_FILE = "data/courses.json"

def insert_evaluation(eval_data):
    evaluations = load_data(FILE)
    students = load_data(STUDENT_FILE)
    courses = load_data(COURSE_FILE)

    # 1. Validate if Evaluation ID is unique
    if not is_unique(evaluations, "id", eval_data["id"]):
        print("❌ Evaluation ID already exists")
        return

    # 2. Validate if Student exists
    student_ids = [s["id"] for s in students]
    if eval_data["student_id"] not in student_ids:
        print(f"❌ Error: Student ID {eval_data['student_id']} does not exist.")
        return

    # 3. Validate if Course exists
    course_ids = [c["id"] for c in courses]
    if eval_data["course_id"] not in course_ids:
        print(f"❌ Error: Course ID {eval_data['course_id']} does not exist.")
        return

    # 4. Save data
    evaluations.append(eval_data)
    save_data(FILE, evaluations)
    print("✅ Marks inserted successfully")

def list_evaluations():
    evals = load_data(FILE)
    if not evals:
        print("No evaluations found.")
        return
    for e in evals:
        print(f"ID: {e['id']} | Student: {e['student_id']} | Course: {e['course_id']} | Marks: {e['marks']}")

def search_eval_by_student(student_id):
    evals = load_data(FILE)
    found = [e for e in evals if e["student_id"] == student_id]
    if not found:
        print(f"❌ No marks found for Student ID {student_id}")
    else:
        for e in found:
            print(e)

def update_evaluation(eval_id, new_marks):
    evals = load_data(FILE)
    for e in evals:
        if e["id"] == eval_id:
            e["marks"] = new_marks
            save_data(FILE, evals)
            print("✅ Marks updated successfully")
            return
    print("❌ Evaluation record not found")

def delete_evaluation(eval_id):
    evals = load_data(FILE)
    new_evals = [e for e in evals if e["id"] != eval_id]
    if len(new_evals) == len(evals):
        print("❌ Evaluation record not found")
        return
    save_data(FILE, new_evals)
    print("✅ Evaluation record deleted")