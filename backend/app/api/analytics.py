from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.db.database import get_db
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet
from app.schemas.analytics_schema import EmployeeROI, ProjectProfit, DepartmentSummary

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/employee-roi", response_model=list[EmployeeROI])
def employee_roi(db: Session = Depends(get_db)):
    # total hours per project for revenue allocation
    project_hours_subq = (
        db.query(
            Timesheet.project_id.label("project_id"),
            func.sum(Timesheet.hours_worked).label("total_project_hours"),
        )
        .group_by(Timesheet.project_id)
        .subquery()
    )

    # compute cost and revenue per employee across all projects
    q = (
        db.query(
            Employee.id.label("employee_id"),
            Employee.name.label("employee_name"),
            Employee.department.label("department"),
            func.sum(Timesheet.hours_worked).label("total_hours"),
            func.sum(Timesheet.hours_worked * Employee.hourly_rate).label("total_cost"),
            func.sum(
                (Timesheet.hours_worked / project_hours_subq.c.total_project_hours)
                * Project.revenue
            ).label("total_revenue"),
        )
        .join(Timesheet, Timesheet.employee_id == Employee.id)
        .join(Project, Project.id == Timesheet.project_id)
        .join(project_hours_subq, project_hours_subq.c.project_id == Timesheet.project_id)
        .group_by(Employee.id, Employee.name, Employee.department)
    )

    results = []
    for row in q.all():
        total_cost = float(row.total_cost or 0)
        total_revenue = float(row.total_revenue or 0)
        roi = (total_revenue / total_cost) if total_cost else None
        results.append(
            EmployeeROI(
                employee_id=row.employee_id,
                employee_name=row.employee_name,
                department=row.department,
                total_hours=float(row.total_hours or 0),
                total_cost=total_cost,
                total_revenue=total_revenue,
                roi=roi,
            )
        )
    return results


@router.get("/project-profit", response_model=list[ProjectProfit])
def project_profit(db: Session = Depends(get_db)):
    # total labor cost per project
    q = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.sum(Timesheet.hours_worked).label("total_hours"),
            func.sum(Timesheet.hours_worked * Employee.hourly_rate).label("total_cost"),
            Project.revenue.label("total_revenue"),
        )
        .join(Timesheet, Timesheet.project_id == Project.id)
        .join(Employee, Employee.id == Timesheet.employee_id)
        .group_by(Project.id, Project.name, Project.revenue)
    )

    results = []
    for row in q.all():
        total_cost = float(row.total_cost or 0)
        total_revenue = float(row.total_revenue or 0)
        profit = total_revenue - total_cost
        profit_margin = (profit / total_revenue) if total_revenue else None
        results.append(
            ProjectProfit(
                project_id=row.project_id,
                project_name=row.project_name,
                total_hours=float(row.total_hours or 0),
                total_cost=total_cost,
                total_revenue=total_revenue,
                profit=profit,
                profit_margin=profit_margin,
            )
        )
    return results


@router.get("/department-summary", response_model=list[DepartmentSummary])
def department_summary(db: Session = Depends(get_db)):
    # Need project hours per project for revenue allocation per timesheet row
    project_hours_subq = (
        db.query(
            Timesheet.project_id.label("project_id"),
            func.sum(Timesheet.hours_worked).label("total_project_hours"),
        )
        .group_by(Timesheet.project_id)
        .subquery()
    )

    q = (
        db.query(
            Employee.department.label("department"),
            func.sum(Timesheet.hours_worked).label("total_hours"),
            func.sum(Timesheet.hours_worked * Employee.hourly_rate).label("total_cost"),
            func.sum(
                (Timesheet.hours_worked / project_hours_subq.c.total_project_hours)
                * Project.revenue
            ).label("total_revenue"),
        )
        .join(Timesheet, Timesheet.employee_id == Employee.id)
        .join(Project, Project.id == Timesheet.project_id)
        .join(project_hours_subq, project_hours_subq.c.project_id == Timesheet.project_id)
        .group_by(Employee.department)
    )

    results = []
    for row in q.all():
        total_cost = float(row.total_cost or 0)
        total_revenue = float(row.total_revenue or 0)
        roi = (total_revenue / total_cost) if total_cost else None
        results.append(
            DepartmentSummary(
                department=row.department,
                total_hours=float(row.total_hours or 0),
                total_cost=total_cost,
                total_revenue=total_revenue,
                roi=roi,
            )
        )
    return results


@router.get("/overall")
def overall(db: Session = Depends(get_db)):
    # total cost = sum(hours * rate)
    total_cost = (
        db.query(func.coalesce(func.sum(Timesheet.hours_worked * Employee.hourly_rate), 0.0))
        .join(Employee, Employee.id == Timesheet.employee_id)
        .scalar()
    )

    # total revenue = sum(Project.revenue) once per project
    total_revenue = db.query(func.coalesce(func.sum(Project.revenue), 0.0)).scalar()

    roi = (float(total_revenue) / float(total_cost)) if total_cost else None
    return {
        "total_cost": float(total_cost or 0),
        "total_revenue": float(total_revenue or 0),
        "roi": roi,
    }


