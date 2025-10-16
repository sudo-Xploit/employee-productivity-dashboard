from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str
    department: str | None = None
    hourly_rate: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
