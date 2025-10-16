from pydantic import BaseModel

class TimesheetBase(BaseModel):
    employee_id: int
    project_id: int
    hours_worked: float

class TimesheetCreate(TimesheetBase):
    pass

class TimesheetResponse(TimesheetBase):
    id: int

    class Config:
        orm_mode = True
