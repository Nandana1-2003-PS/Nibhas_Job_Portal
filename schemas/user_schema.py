# schemas/user_schema.py
from pydantic import BaseModel, Field
from typing import List
from schemas.skill_schema import SkillBase  # Add this import

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
    skills: List[SkillBase] = []  # Add this field

    class Config:
        from_attributes = True


class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., max_length=72)
    
    class Config:
        from_attributes = True        