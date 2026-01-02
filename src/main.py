from students import insert_student, list_students, search_student_by_name
from projects import (
    insert_project,
    search_project_by_id,
    search_project_by_title,
    update_project,
    delete_project,
)
from reports import (
    get_student_performance_report,
    get_subject_analytics,
    global_grade_distribution,
    student_consistency_report,
    department_battle_stats
)
from courses import (
    insert_course,
    list_courses,
    update_course,
    delete_course,
)

from evaluation import (
    insert_evaluation, 
    list_evaluations, 
    search_eval_by_student, 
    update_evaluation, 
    delete_evaluation
)


def main_menu():
    print("""
1. Students
2. Projects
3. courses
4. Reports
5. Evaluations (Marks)
0. Exit
""")


def students_menu():
    while True:
        print("""
Students:
1. Insert Student
2. List Students
3. Search Student by Name
0. Back
""")
        op = input("Choice: ")
        if op == "1":
            try:
                student = {
                    "id": int(input("ID: ")),
                    "name": input("Name: "),
                    "email": input("Email: "),
                    "course": input("Course: "),
                    "year": int(input("Year: ")),
                }
            except ValueError:
                print("❌ Invalid number")
                continue
            insert_student(student)
        elif op == "2":
            list_students()
        elif op == "3":
            search_student_by_name(input("Name: "))
        elif op == "0":
            break
        else:
            print("Invalid option")


def projects_menu():
    while True:
        print("""
Projects:
1. Insert Project
2. Search Project by ID
3. Search Project by Title
4. Update Project
5. Delete Project
0. Back
""")
        op = input("Choice: ")
        if op == "1":
            try:
                project = {
                    "id": int(input("ID: ")),
                    "title": input("Title: "),
                    "description": input("Description: "),
                    "status": input("Status: "),
                    "supervisor_id": int(input("Supervisor ID: ")),
                    "student_ids": [list(map(int, input("Student IDs (comma separated): ").split(",")))],
                }
            except ValueError:
                print("❌ Invalid number")
                continue
            insert_project(project)
        elif op == "2":
            try:
                pid = int(input("Project ID: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            search_project_by_id(pid)
        elif op == "3":
            search_project_by_title(input("Search text: "))
        elif op == "4":
            try:
                pid = int(input("Project ID to update: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            new_title = input("New Title (leave blank to skip): ")
            new_description = input("New Description (leave blank to skip): ")
            new_status = input("New Status (leave blank to skip): ")
            new_supervisor = input("New Supervisor ID (leave blank to skip): ")
            new_students = input("New Student IDs (comma separated, leave blank to skip): ")
            new_data = {}
            if new_title:
                new_data["title"] = new_title
            if new_description:
                new_data["description"] = new_description
            if new_status:
                new_data["status"] = new_status
            if new_supervisor:
                try:
                    new_data["supervisor_id"] = int(new_supervisor)
                except ValueError:
                    print("❌ Invalid supervisor ID")
                    continue
            if new_students:
                try:
                    new_data["student_ids"] = list(map(int, new_students.split(",")))
                except ValueError:
                    print("❌ Invalid student IDs")
                    continue
            update_project(pid, new_data)
        elif op == "5":
            try:
                pid = int(input("Project ID to delete: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            delete_project(pid)
        elif op == "0":
            break
        else:
            print("Invalid option")


def courses_menu():
    while True:
        print("""
courses:
1. Insert course
2. List courses
3. Update course
4. Delete course
0. Back
""")
        op = input("Choice: ")
        if op == "1":
            try:
                disciplina = {
                    "id": int(input("ID: ")),
                    "name": input("Name: "),
                    "teacher_id": int(input("Teacher ID: ")),
                }
            except ValueError:
                print("❌ Invalid number")
                continue
            insert_course(disciplina)
        elif op == "2":
            list_courses()
        elif op == "3":
            try:
                disciplina_id = int(input("course ID to update: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            new_name = input("New Name (leave blank to skip): ")
            teacher_id = input("New Teacher ID (leave blank to skip): ")
            new_data = {}
            if new_name:
                new_data["name"] = new_name
            if teacher_id:
                new_data["teacher_id"] = int(teacher_id)
            update_course(disciplina_id, new_data)
        elif op == "4":
            try:
                disciplina_id = int(input("course ID to delete: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            delete_course(disciplina_id)
        elif op == "0":
            break
        else:
            print("Invalid option")


def reports_menu():
    while True:
        print("""
University Intelligence & Analytics:
1. Student Performance Deep-Dive (Search by Student ID)
2. Subject Overall Analytics (Search by Course ID)
3. Student Consistency Index (Top 5)
4. Department Battle Stats
5. Global Grade Distribution
0. Back
""")
        op = input("Option: ")
        
        if op == "1":
            try:
                sid = int(input("Enter Student ID: "))
                get_student_performance_report(sid)
            except ValueError:
                print("❌ Please enter a numeric ID")
        elif op == "2":
            try:
                cid = int(input("Enter Course ID: "))
                get_subject_analytics(cid)
            except ValueError:
                print("❌ Please enter a numeric ID")
        elif op == "3":
            student_consistency_report()
        elif op == "4":
            department_battle_stats()
        elif op == "5":
            global_grade_distribution()
        elif op == "0":
            break

def evaluation_menu():
    while True:
        print("""
Evaluations (Marks):
1. Insert Marks
2. List All Evaluations
3. View Marks by Student ID
4. Update Marks
5. Delete Evaluation Record
0. Back
""")
        op = input("Choice: ")
        if op == "1":
            try:
                eval_data = {
                    "id": int(input("Evaluation Record ID: ")),
                    "student_id": int(input("Student ID: ")),
                    "course_id": int(input("Course ID: ")),
                    "marks": float(input("Marks: "))
                }
                insert_evaluation(eval_data)
            except ValueError:
                print("❌ Please enter valid numbers")
        elif op == "2":
            list_evaluations()
        elif op == "3":
            try:
                sid = int(input("Enter Student ID: "))
                search_eval_by_student(sid)
            except ValueError:
                print("❌ Invalid ID")
        elif op == "4":
            try:
                eid = int(input("Evaluation Record ID to update: "))
                new_m = float(input("New Marks: "))
                update_evaluation(eid, new_m)
            except ValueError:
                print("❌ Invalid input")
        elif op == "5":
            try:
                eid = int(input("Evaluation Record ID to delete: "))
                delete_evaluation(eid)
            except ValueError:
                print("❌ Invalid ID")
        elif op == "0":
            break


if __name__ == "__main__":
    while True:
        main_menu()
        op = input("Option: ")
        if op == "1":
            students_menu()
        elif op == "2":
            projects_menu()
        elif op == "3":
            courses_menu()
        elif op == "4":
            reports_menu()
        elif op == "5":
            evaluation_menu()
        elif op == "0":
            break
        else:
            print("Invalid option")
