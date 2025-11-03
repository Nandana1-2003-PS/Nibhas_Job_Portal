from pydantic import BaseModel

class PreferredJobBase(BaseModel):
    job_title: str
    location: str
    salary_expectation: str
    job_type: str

class PreferredJobCreate(PreferredJobBase):
    pass

class PreferredJobUpdate(BaseModel):
    job_title: str | None = None
    location: str | None = None
    salary_expectation: str | None = None
    job_type: str | None = None

class PreferredJobResponse(PreferredJobBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
