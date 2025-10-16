from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import employee, project, timesheet
from app.api import upload, employees, projects, timesheets, analytics, reports

app = FastAPI(title="Employee Productivity & Cost Dashboard API")

# create DB tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(upload.router)
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(timesheets.router)
app.include_router(analytics.router)
app.include_router(reports.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend running successfully!"}
