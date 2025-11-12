from pydantic import BaseModel
from typing import List

class SkillCreate(BaseModel):
    name: str

class SkillBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserSkillsUpdate(BaseModel):
    skill_ids: List[int]

class UserSkillsResponse(BaseModel):
    id: int
    username: str
    email: str
    skills: List[SkillBase]

    class Config:
        from_attributes = True