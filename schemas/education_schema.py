from pydantic import BaseModel

# Base schema (shared fields)
class EducationBase(BaseModel):
    qualification: str
    institution: str
    year_of_passing: str

# Schema for creating new education records
class EducationCreate(EducationBase):
    pass

# Response schema (includes id + user_id)
class EducationResponse(EducationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
