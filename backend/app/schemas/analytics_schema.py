from pydantic import BaseModel


class EmployeeROI(BaseModel):
    employee_id: int
    employee_name: str
    department: str | None = None
    total_hours: float
    total_cost: float
    total_revenue: float
    roi: float | None = None


class ProjectProfit(BaseModel):
    project_id: int
    project_name: str
    total_hours: float
    total_cost: float
    total_revenue: float
    profit: float
    profit_margin: float | None = None


class DepartmentSummary(BaseModel):
    department: str | None = None
    total_hours: float
    total_cost: float
    total_revenue: float
    roi: float | None = None

