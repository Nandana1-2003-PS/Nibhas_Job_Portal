from pydantic import BaseModel

class EmployerJobCreate(BaseModel):
    job_title: str
    description: str
    location: str
    salary: str | None = None
    vaccancy:int
    job_type: str | None = None

class EmployerJobUpdate(BaseModel):
    job_title: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    vaccancy:int
    job_type: str | None = None

class EmployerJobResponse(BaseModel):
    id: int
    job_title: str
    description: str
    location: str
    salary: str | None
    vaccancy:int
    job_type: str | None
    employer_id: int

    class Config:
        from_attributes = True
