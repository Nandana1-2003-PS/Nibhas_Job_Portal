from pydantic import BaseModel
from datetime import datetime

class JobPostCreate(BaseModel):
    job_title: str
    description: str
    salary: str | None = None
    job_type: str | None = None
    vacancies: int | None = None
    location: str | None = None

class JobPostResponse(JobPostCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
