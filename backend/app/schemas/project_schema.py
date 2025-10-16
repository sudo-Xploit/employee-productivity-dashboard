from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    revenue: float

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int

    class Config:
        orm_mode = True
