from pydantic import BaseModel

class EducationBase(BaseModel):
    qualification: str
    institution: str
    year_of_passing: str

class EducationCreate(EducationBase):
    pass
class EducationResponse(EducationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
