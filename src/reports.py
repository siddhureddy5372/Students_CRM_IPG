import time
import statistics
from storage import load_data


EVAL_FILE = "data/evaluation.json"
STUDENT_FILE = "data/students.json"
COURSE_FILE = "data/courses.json"

def get_student_performance_report(student_id):
    print("\nGenerating student performance report...")
    time.sleep(1)
    """Deep dive into a single student's academic standing."""
    evals = load_data(EVAL_FILE)
    students = load_data(STUDENT_FILE)
    courses = load_data(COURSE_FILE)
    
    # Find student info
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print(f"❌ Student ID {student_id} not found.")
        return

    student_evals = [e for e in evals if e["student_id"] == student_id]
    
    print(f"\n🚀 --- INTELLIGENCE REPORT: {student['name'].upper()} ---")
    print(f"Course: {student['course']} | Year: {student['year']}")
    
    if not student_evals:
        print("📊 No academic data available for this student yet.")
        return

    # Calculations
    marks = [e["marks"] for e in student_evals]
    avg_mark = sum(marks) / len(marks)
    highest = max(marks)
    passed = len([m for m in marks if m >= 10])
    
    print(f"📈 GPA Equivalent: {avg_mark:.2f}/20")
    print(f"🏆 Best Performance: {highest}")
    print(f"✅ Pass Rate: {(passed/len(marks))*100:.1f}%")
    print("-" * 40)
    
    # Detail per subject
    course_map = {c["id"]: c["name"] for c in courses}
    for e in student_evals:
        c_name = course_map.get(e["course_id"], "Unknown Course")
        status = "PASS" if e["marks"] >= 10 else "FAIL"
        print(f"[{status}] {c_name}: {e['marks']}")

def subject_difficulty_ranking():
    evals = load_data(EVAL_FILE)
    courses = load_data(COURSE_FILE)
    
    stats = []
    course_map = {c["id"]: c["name"] for c in courses}

    for c_id, c_name in course_map.items():
        c_evals = [e["marks"] for e in evals if e["course_id"] == c_id]
        if not c_evals: continue
        
        failure_rate = (len([m for m in c_evals if m < 10]) / len(c_evals)) * 100
        avg = sum(c_evals) / len(c_evals)
        stats.append({"name": c_name, "fail": failure_rate, "avg": avg})

    # Sort by highest failure rate
    stats.sort(key=lambda x: x['fail'], reverse=True)

    print("\n🔥 --- SUBJECT DIFFICULTY RANKING ---")
    for s in stats:
        emoji = "🔴" if s['fail'] > 20 else "🟢"
        print(f"{emoji} {s['name']:<30} | Fail Rate: {s['fail']:>5.1f}% | Avg: {s['avg']:.2f}")


def department_battle_stats():
    evals = load_data(EVAL_FILE)
    students = load_data(STUDENT_FILE)
    
    dept_stats = {} # { "LCDIA": [marks], "LEI": [marks] }
    student_dept = {s["id"]: s["course"] for s in students}

    for e in evals:
        dept = student_dept.get(e["student_id"])
        if dept:
            dept_stats.setdefault(dept, []).append(e["marks"])

    print("\n🏛️ --- DEPARTMENT PERFORMANCE BATTLE ---")
    for dept, marks in dept_stats.items():
        avg = sum(marks) / len(marks)
        top_performance = max(marks)
        print(f"Department {dept:6}: Avg {avg:.2f} | Record High: {top_performance}")


def student_consistency_report():
    evals = load_data(EVAL_FILE)
    students = load_data(STUDENT_FILE)
    
    print("\n🎯 --- STUDENT CONSISTENCY INDEX (Top 5) ---")
    student_marks = {}
    for e in evals:
        student_marks.setdefault(e["student_id"], []).append(e["marks"])

    consistency_list = []
    for s_id, marks in student_marks.items():
        if len(marks) > 1:
            name = next(s["name"] for s in students if s["id"] == s_id)
            # Standard Deviation: Lower means more consistent
            std_dev = statistics.stdev(marks) 
            avg = sum(marks) / len(marks)
            consistency_list.append({"name": name, "dev": std_dev, "avg": avg})

    # Sort by lowest deviation (most consistent)
    consistency_list.sort(key=lambda x: x['dev'])
    for s in consistency_list[:5]:
        print(f"{s['name']:<20} | Consistency Score: {100 - (s['dev']*10):.1f}/100 | Avg: {s['avg']:.2f}")


def global_grade_distribution():
    evals = load_data(EVAL_FILE)
    marks = [e["marks"] for e in evals]
    
    ranges = {"0-5": 0, "6-9": 0, "10-13": 0, "14-17": 0, "18-20": 0}
    for m in marks:
        if m < 6: ranges["0-5"] += 1
        elif m < 10: ranges["6-9"] += 1
        elif m < 14: ranges["10-13"] += 1
        elif m < 18: ranges["14-17"] += 1
        else: ranges["18-20"] += 1

    print("\n🌐 --- GLOBAL GRADE DISTRIBUTION ---")
    for r, count in ranges.items():
        bar = "█" * count
        print(f"{r:>6} | {bar} ({count})")


def get_subject_analytics(course_id):
    """High-level analytics for a specific subject across all students."""
    evals = load_data(EVAL_FILE)
    courses = load_data(COURSE_FILE)
    
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        print("❌ Course not found.")
        return

    course_evals = [e for e in evals if e["course_id"] == course_id]
    
    print(f"\n🔬 --- SUBJECT ANALYTICS: {course['name'].upper()} ---")
    
    if not course_evals:
        print("📊 No data recorded for this subject.")
        return

    marks = [e["marks"] for e in course_evals]
    avg = sum(marks) / len(marks)
    failure_rate = (len([m for m in marks if m < 10]) / len(marks)) * 100

    print(f"👥 Total Students Evaluated: {len(course_evals)}")
    print(f"📊 Class Average: {avg:.2f}")
    print(f"⚠️ Failure Risk: {failure_rate:.1f}%")
    
    # Visualization-style bar
    bar_size = int(avg)
    print(f"Performance Bar: [{'#' * bar_size}{'-' * (20-bar_size)}] {avg}/20")