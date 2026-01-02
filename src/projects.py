from storage import load_data, save_data
from validations import is_unique, not_empty

FILE = "data/projects.json"
TEACHERS_FILE = "data/teachers.json"

def insert_project(project):
    projects = load_data(FILE)

    if not is_unique(projects, "id", project["id"]):
        print("❌ Project ID already exists")
        return

    if not not_empty(project["title"]):
        print("❌ Title cannot be empty")
        return

    teachers = load_data(TEACHERS_FILE)
    supervisor_exists = False
    for t in teachers:
        if t["id"] == project["supervisor_id"]:
            supervisor_exists = True
            break
    
    if not supervisor_exists:
        print("❌ Error: Supervisor ID does not exist.")
        return

    projects.append(project)
    save_data(FILE, projects)
    print("✅ Project added")

def search_project_by_id(pid):
    projects = load_data(FILE)
    for p in projects:
        if p["id"] == pid:
            print(p)
            return
    print("❌ Project not found")

def search_project_by_title(text):
    projects = load_data(FILE)
    for p in projects:
        if text.lower() in p["title"].lower():
            print(p)

def update_project(project_id, new_data):
    projects = load_data(FILE)

    for p in projects:
        if p["id"] == project_id:
            if "title" in new_data and not not_empty(new_data["title"]):
                print("❌ Title cannot be empty")
                return

            p.update(new_data)
            save_data(FILE, projects)
            print("✅ Project updated")
            return

    print("❌ Project not found")


def delete_project(project_id):
    projects = load_data(FILE)
    new_projects = [p for p in projects if p["id"] != project_id]

    if len(new_projects) == len(projects):
        print("❌ Project not found")
        return

    save_data(FILE, new_projects)
    print("✅ Project deleted")
