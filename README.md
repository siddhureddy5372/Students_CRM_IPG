
# 🎓 UniIntelligence (IPG) | Student Analytics CRM & Dashboard

UniIntelligence is a professional **Student Relationship Management (CRM)** and analytics platform designed for academic tracking. The system uses a JSON-based database architecture and a Python-driven static site generator to create a high-performance, dark-themed dashboard.

## 🚀 System Architecture

The project operates through a dual-process workflow:

1.  **Backend CRM (`main.py`)**: A command-line interface to manage data. To ensure data integrity, the system allows editing marks while keeping the **Student** and **Subject** fixed (Read-Only).
2.  **Frontend Generator (`web_generator.py`)**: A powerful engine that processes raw JSON data and generates a modern, responsive analytics dashboard in the `dashboard/` folder.

---

## 📂 Project Structure

* **`data/`**: The "Single Source of Truth." Stores `students.json`, `evaluation.json`, `projects.json`, `courses.json`, and `teachers.json`.
* **`src/`**: 
    * `main.py`: The management console for adding/editing records.
    * `web_generator.py`: The UI builder that outputs the HTML files.
    * `storage.py`: Handles secure read/write operations for the JSON files.
* **`dashboard/`**: The generated web platform.
    * `index.html`: Student progress reports with interactive analytics modals.
    * `projects.html`: Active/Inactive project tracking and team assignments.
    * `evaluations.html`: A "Google Keep" style grid of all student marks.

---

## 🛠️ Getting Started

### 1. Data Management
To update grades or add new students, run the CRM:
```bash
python main.py

```

> **Note:** When editing an evaluation, the Student and Subject are locked to prevent accidental data corruption. You only update the mark.

### 2. Update the Dashboard

After any change to the JSON files, regenerate the frontend:

```bash
python web_generator.py

```

### 3. View Analytics

Open `dashboard/index.html` in any modern web browser to view the updated analytics.

---

## ✨ Key Features

* **Professional Dark UI**: Indigo-tinted theme with "Plus Jakarta Sans" typography.
* **Smart Analytics**: Automatic calculation of **Pass Rates**, **Best/Worst Marks**, and **Student Reliability** (Consistency).
* **Note-Style Evaluations**: The "All Marks" page utilizes a modern masonry grid layout with high-contrast PASS/FAIL badges.
* **Interactive Modals**: Detailed subject-by-subject percentile breakdowns for every student.
* **Real-time Search**: Client-side JavaScript filtering to find students instantly by name.
* **Project Oversight**: Tracks project statuses, student teams, and academic supervisors.

---

## 🧪 Technical Requirements

* **Python 3.x**
* **Bootstrap 5.3** (Loaded via CDN)
* **No external database** (Uses lightweight JSON flat-files)

