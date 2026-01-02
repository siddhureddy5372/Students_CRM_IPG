import json
import os
import statistics
import sys
from storage import load_data

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

STUDENT_FILE = "data/students.json"
EVAL_FILE = "data/evaluation.json"
PROJECT_FILE = "data/projects.json"
COURSE_FILE = "data/courses.json"
TEACHER_FILE = "data/teachers.json"
DASHBOARD_PATH = "../dashboard/"

def calculate_percentile(all_marks_in_subject, student_mark):
    if not all_marks_in_subject: return 0
    less_than = len([m for m in all_marks_in_subject if m < student_mark])
    return (less_than / len(all_marks_in_subject)) * 100

# SHARED PROFESSIONAL HEAD - FIXES ALL VISIBILITY ISSUES
HTML_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniIntelligence | Student Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #0b0f1a;
            --card-bg: #161b2b;
            --card-hover: #1e253a;
            --border-color: #2d364f;
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
            --accent-primary: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.15);
        }

        body { 
            background-color: var(--bg-body); 
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* Navbar Visibility */
        .navbar { 
            background: rgba(11, 15, 26, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1.2rem 0;
        }
        .nav-link { color: var(--text-main) !important; font-weight: 600; margin-left: 20px; }
        .nav-link:hover { color: var(--accent-primary) !important; }

        /* Card Visibility Fixes */
        .report-card, .consistent-card { 
            background: var(--card-bg); 
            border-radius: 20px; 
            border: 1px solid var(--border-color);
            padding: 30px;
            margin-bottom: 24px;
            color: var(--text-main);
            transition: all 0.3s ease;
        }
        .report-card:hover { border-color: var(--accent-primary); transform: translateY(-5px); }

        /* Global Text Fixes */
        h1, h2, h3, h4, h5, strong { color: var(--text-main) !important; }
        .text-muted, .text-dim, small { color: var(--text-dim) !important; }

        /* Table Visibility Fixes for All Marks page */
        .table { color: var(--text-main) !important; margin-top: 20px; border-color: var(--border-color); }
        .table thead th { color: var(--accent-primary) !important; border-bottom: 2px solid var(--border-color); }
        .table td { border-bottom: 1px solid var(--border-color); vertical-align: middle; }
        
        /* Modal Fix */
        .modal-content { background: #111827; color: var(--text-main); border: 1px solid var(--border-color); border-radius: 28px; }

        .search-container { max-width: 600px; margin: 40px auto; position: relative; }
        .search-input {
            background: var(--card-bg); border: 1px solid var(--border-color);
            color: white; padding: 15px 25px; border-radius: 12px; width: 100%;
        }
        .student-initials {
            width: 48px; height: 48px; background: var(--accent-primary);
            border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; margin-right: 15px;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    <div class="container">
        <a class="navbar-brand d-flex align-items-center" href="index.html">
            <div class="me-2" style="color: var(--accent-primary)">◈</div> 
            <strong>UniIntelligence(IPG)</strong>
        </a>
        <div class="navbar-nav ms-auto">
            <a class="nav-link" href="index.html">Progress Reports</a>
            <a class="nav-link" href="projects.html">Projects</a>
            <a class="nav-link" href="evaluations.html">All Marks</a>
        </div>
    </div>
</nav>
<div class="container mt-4">
"""

HTML_FOOTER = """
</div> 
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
function filterStudents() {
    let input = document.getElementById('studentSearch').value.toLowerCase();
    let cards = document.getElementsByClassName('student-col');
    for (let i = 0; i < cards.length; i++) {
        let name = cards[i].getAttribute('data-name').toLowerCase();
        cards[i].style.display = name.includes(input) ? "" : "none";
    }
}
function showDetails(data) {
    document.getElementById('m-name').innerText = data.name;
    document.getElementById('m-pass').innerText = data.passRate + '%';
    document.getElementById('m-best').innerText = data.best;
    document.getElementById('m-worst').innerText = data.worst;
    document.getElementById('m-const').innerText = data.consistency;
    let pnl = document.getElementById('m-percentiles');
    pnl.innerHTML = '';
    data.subjects.forEach(s => {
        pnl.innerHTML += `
            <div class="mb-4">
                <div class="d-flex justify-content-between mb-2">
                    <span class="fw-bold">${s.name}</span>
                    <span style="color: var(--accent-primary)">Top ${Math.round(100 - s.p)}%</span>
                </div>
                <div class="progress" style="background:#374151;height:8px;"><div class="progress-bar" style="width: ${s.p}%; background: var(--accent-primary)"></div></div>
            </div>`;
    });
    new bootstrap.Modal(document.getElementById('studentModal')).show();
}
</script>
</body></html>
"""

# Rest of the Modal HTML is added specifically to index.html to keep other pages clean
MODAL_HTML = """
<div class="modal fade" id="studentModal" tabindex="-1">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <div class="modal-content p-3">
      <div class="modal-header border-0">
        <h2 class="fw-800" id="m-name"></h2>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <div class="row g-3 mb-5">
            <div class="col-md-3"><div class="consistent-card text-center p-3 m-0"><small class="text-dim d-block">Pass Rate</small><h4 id="m-pass" class="mb-0"></h4></div></div>
            <div class="col-md-3"><div class="consistent-card text-center p-3 m-0"><small class="text-dim d-block">Best Mark</small><h4 id="m-best" class="mb-0"></h4></div></div>
            <div class="col-md-3"><div class="consistent-card text-center p-3 m-0"><small class="text-dim d-block">Worst Mark</small><h4 id="m-worst" class="mb-0"></h4></div></div>
            <div class="col-md-3"><div class="consistent-card text-center p-3 m-0"><small class="text-dim d-block">Reliability</small><h4 id="m-const" class="mb-0"></h4></div></div>
        </div>
        <h5>Subject Percentiles</h5>
        <div id="m-percentiles" class="mt-4"></div>
      </div>
    </div>
  </div>
</div>
"""

def generate_student_reports_html():
    students = load_data(STUDENT_FILE)
    evals = load_data(EVAL_FILE)
    courses = load_data(COURSE_FILE)
    course_map = {c["id"]: c["name"] for c in courses}
    students.sort(key=lambda x: x['name'])

    body = '<div class="search-container"><input type="text" id="studentSearch" class="search-input" placeholder="Search for a student..." onkeyup="filterStudents()"></div>'
    body += '<div class="row" id="studentContainer">'

    for s in students:
        s_evals = [e for e in evals if e["student_id"] == s["id"]]
        marks = [m['marks'] for m in s_evals]
        best = max(marks) if marks else 0
        worst = min(marks) if marks else 0
        pass_rate = (len([m for m in marks if m >= 10]) / len(marks) * 100) if marks else 0
        consistency = round(100 - (statistics.stdev(marks) * 10), 1) if len(marks) > 1 else "N/A"

        subj_data = []
        for e in s_evals:
            all_m = [x['marks'] for x in evals if x['course_id'] == e['course_id']]
            perc = calculate_percentile(all_m, e['marks'])
            subj_data.append({"name": course_map.get(e['course_id']), "p": perc})

        js_data_json = json.dumps({"name": s['name'], "passRate": round(pass_rate, 1), "best": best, "worst": worst, "consistency": consistency, "subjects": subj_data}).replace("'", "&#39;")
        initials = "".join([n[0] for n in s['name'].split()[:2]])

        body += f"""
        <div class="col-md-6 student-col" data-name="{s['name']}">
            <div class="report-card" onclick='showDetails({js_data_json})'>
                <div class="d-flex align-items-center mb-3">
                    <div class="student-initials">{initials}</div>
                    <div><h4 class="mb-0">{s['name']}</h4><small class="text-dim">{s['course']} • Year {s['year']}</small></div>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge" style="background:var(--accent-glow);color:var(--accent-primary);border:1px solid var(--accent-primary)">View Analytics</span>
                    <span class="text-dim">Avg: {(sum(marks)/len(marks) if marks else 0):.2f}</span>
                </div>
            </div>
        </div>"""
    
    with open(os.path.join(DASHBOARD_PATH, "index.html"), "w", encoding="utf-8") as f:
        f.write(HTML_HEAD + body + "</div>" + MODAL_HTML + HTML_FOOTER)

def generate_evaluations_html():
    evals = load_data(EVAL_FILE)
    courses = {c["id"]: c["name"] for c in load_data(COURSE_FILE)}
    students = {s["id"]: s["name"] for s in load_data(STUDENT_FILE)}
    
    # Header for the page
    content = '<h2 class="mb-5 fw-800">Global Evaluation Log</h2>'
    content += '<div class="row g-4">' # Bootstrap grid for the "Note" boxes
    
    for e in reversed(evals):
        is_pass = e['marks'] >= 10
        status = "PASS" if is_pass else "FAIL"
        # Using your palette: Green for pass, Red for fail
        accent_color = "#22c55e" if is_pass else "#ef4444"
        glow_bg = "rgba(34, 197, 94, 0.1)" if is_pass else "rgba(239, 68, 68, 0.1)"
        
        content += f"""
        <div class="col-md-4 col-lg-3">
            <div class="consistent-card h-100" style="border-top: 4px solid {accent_color}; transition: transform 0.2s;">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge" style="background:{glow_bg}; color:{accent_color}; border: 1px solid {accent_color}">{status}</span>
                    <h3 class="mb-0" style="color: var(--text-main); font-size: 1.5rem;">{e['marks']}<small class="text-dim" style="font-size: 0.8rem;">/20</small></h3>
                </div>
                <h5 class="fw-bold mb-1">{students.get(e['student_id'], 'Unknown Student')}</h5>
                <p class="text-dim small mb-0">{courses.get(e['course_id'], 'Unknown Subject')}</p>
            </div>
        </div>
        """
    
    content += "</div>"
    
    with open(os.path.join(DASHBOARD_PATH, "evaluations.html"), "w", encoding="utf-8") as f:
        f.write(HTML_HEAD + content + HTML_FOOTER)


def generate_projects_html():
    projects = load_data(PROJECT_FILE)
    students = {s["id"]: s["name"] for s in load_data(STUDENT_FILE)}
    teachers = {t["id"]: t["name"] for t in load_data(TEACHER_FILE)}
    
    row_content = "<h2>Active Projects</h2><div class='row'>"
    for p in projects:
        t_name = teachers.get(p['supervisor_id'], "N/A")
        s_names = ", ".join([students.get(sid, "N/A") for sid in p.get('student_ids', [])])
        row_content += f"""
        <div class="col-md-6"><div class="consistent-card">
            <h4 style="color:var(--accent-primary) !important;">{p['title']}</h4>
            <p class="text-dim small">{p['description']}</p>
            <div class="mb-2"><strong>Students:</strong> {s_names}</div>
            <div class="d-flex justify-content-between align-items-center mt-3">
                <span class="badge" style="background:var(--accent-glow);color:var(--accent-primary)">{p['status']}</span>
                <small class="text-dim">Supervisor: {t_name}</small>
            </div>
        </div></div>"""
    
    with open(os.path.join(DASHBOARD_PATH, "projects.html"), "w", encoding="utf-8") as f:
        f.write(HTML_HEAD + row_content + "</div>" + HTML_FOOTER)

if __name__ == "__main__":
    os.makedirs(DASHBOARD_PATH, exist_ok=True)
    generate_student_reports_html()
    generate_evaluations_html()
    generate_projects_html()
    print("Dashboard Updated Successfully!")