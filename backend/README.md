# Employee Productivity & Cost Dashboard

A backend-driven analytics system that consolidates employee timesheets, payroll, and project revenue data to calculate real-time ROI, profitability, and performance insights.

---

## 🚀 Overview

This project helps business owners and managers identify which employees, tasks, and departments are profitable versus wasteful. The system connects timesheet, payroll, and revenue data to produce actionable metrics like employee ROI, project profit margins, and departmental summaries.

The backend is built with **FastAPI (Python)** and **SQLite**, offering modular design, clean data handling, and easy future integration with frontend dashboards.

---

## 📂 Project Structure

```
backend/
│
├── app/
│   ├── main.py                   # FastAPI entry point
│   ├── db/
│   │   ├── database.py            # Database connection and session setup
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── employee.py
│   │   ├── project.py
│   │   └── timesheet.py
│   ├── schemas/                   # Pydantic validation models
│   │   ├── employee_schema.py
│   │   ├── project_schema.py
│   │   └── timesheet_schema.py
│   ├── api/                       # FastAPI route modules
│   │   ├── upload.py
│   │   ├── employees.py
│   │   ├── projects.py
│   │   ├── timesheets.py
│   │   ├── analytics.py
│   │   └── reports.py
│   └── utils/                     # Helper utilities
│       ├── csv_loader.py
│       └── report_generator.py
│
├── employee_dashboard.db          # SQLite database
├── requirements.txt               # Python dependencies
└── venv/                          # Virtual environment
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sudo-Xploit/employee-productivity-dashboard.git
cd employee-productivity-dashboard/backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

Visit the API documentation at:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧩 Features

### ✅ Core Modules

| Module        | Description                                              |
| ------------- | -------------------------------------------------------- |
| Upload System | Upload CSV files for employees, projects, and timesheets |
| CRUD APIs     | Manage employee, project, and timesheet data             |
| Analytics     | Compute ROI, profit margins, and department summaries    |
| Reporting     | Export insights to Excel and PDF reports                 |

---

## 📊 API Endpoints

### **Base URL:** `http://127.0.0.1:8000`

| Endpoint                        | Method | Description                               |
| ------------------------------- | ------ | ----------------------------------------- |
| `/`                             | GET    | Health check (returns backend status)     |
| `/upload/employees`             | POST   | Upload employee CSV                       |
| `/upload/projects`              | POST   | Upload project CSV                        |
| `/upload/timesheets`            | POST   | Upload timesheet CSV                      |
| `/analytics/employee-roi`       | GET    | ROI per employee                          |
| `/analytics/project-profit`     | GET    | Profitability per project                 |
| `/analytics/department-summary` | GET    | ROI summary by department                 |
| `/analytics/overall`            | GET    | Overall ROI and cost summary              |
| `/report/excel`                 | GET    | Download analytics report in Excel format |
| `/report/pdf`                   | GET    | Download analytics report in PDF format   |

---

## 📄 Sample Data Format

### employees.csv

```
id,name,department,hourly_rate
1,John Doe,Marketing,30
2,Jane Smith,Design,28
3,Alex Johnson,Development,40
4,Sarah Lee,Development,35
```

### projects.csv

```
id,name,revenue
1,Website Redesign,15000
2,Ad Campaign,20000
3,SEO Campaign,8000
```

### timesheets.csv

```
id,employee_id,project_id,hours_worked
1,1,2,10
2,2,1,15
3,3,3,20
4,4,2,30
```

---

## 🧠 Analytics Metrics

| Metric                    | Description                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| **Employee ROI**          | Measures how much revenue each employee generates compared to their cost |
| **Project Profitability** | Determines total cost vs. revenue for each project                       |
| **Department Summary**    | Aggregated hours, cost, and ROI for each department                      |
| **Overall ROI**           | Total return on investment for the entire organization                   |

---

## 📦 Report Generation

### **Endpoints**

* `/report/excel` → Returns Excel file (`.xlsx`)
* `/report/pdf` → Returns PDF report

### **Libraries Used**

* **OpenPyXL** → Excel file creation
* **ReportLab** → PDF report generation

---

## 🧪 Testing Instructions

1. Upload all three CSV files via Swagger UI.
2. Visit each analytics endpoint to verify results.
3. Test report download endpoints.
4. Inspect `employee_dashboard.db` to confirm data integrity.

---

## 🔒 Future Enhancements

* Add JWT-based authentication
* Implement user roles and access control
* Create React/Next.js frontend for visualization
* Automate weekly report generation
* Migrate database from SQLite → PostgreSQL for scalability

---

## 👨‍💻 Contributors

* **Muhammad Huzaifa** — Project Developer

---

## 🏁 Conclusion

This project demonstrates how to transform raw operational data into actionable intelligence. It establishes a solid backend foundation for future SaaS dashboards, helping service-based businesses optimize performance, cut waste, and improve profitability.
