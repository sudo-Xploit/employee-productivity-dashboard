from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.database import Base

class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    hours_worked = Column(Float, nullable=False)
