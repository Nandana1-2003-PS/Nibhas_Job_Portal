# schemas/user_schema.py
from pydantic import BaseModel, Field,EmailStr
from typing import List
from schemas.skill_schema import SkillBase  
from schemas.skill_schema import SkillBase, SkillCreate
from schemas.education_schema import EducationCreate, EducationResponse
from schemas.preferred_schemas import PreferredJobCreate, PreferredJobResponse
from schemas.personal_details_schema import PersonalDetailsCreate, PersonalDetailsResponse

class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., max_length=72)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    skills: List[SkillBase] = []  

    class Config:
        from_attributes = True


