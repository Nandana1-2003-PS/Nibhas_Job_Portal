from pydantic import BaseModel, Field
from typing import List, Optional
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

class UserBase(BaseModel):
    username: str
    email: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    personal_details: Optional[PersonalDetailsResponse] = None
    education: List[EducationResponse] = []
    preferred_jobs: Optional[PreferredJobResponse] = None
    skills: List[SkillBase] = []

    class Config:
        from_attributes = True


class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., max_length=72)

    personal_details: PersonalDetailsCreate
    education: EducationCreate
    preferred_jobs: PreferredJobCreate
    skills: SkillCreate

    class Config:
        from_attributes = True