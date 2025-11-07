from pydantic import BaseModel

class EmployerJobCreate(BaseModel):
    title: str
    description: str
    location: str
    salary: str | None = None
    job_type: str | None = None

class EmployerJobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    job_type: str | None = None

class EmployerJobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    salary: str | None
    job_type: str | None
    employer_id: int

    class Config:
        from_attributes = True
