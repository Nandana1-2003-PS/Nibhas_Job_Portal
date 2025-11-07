from pydantic import BaseModel
from datetime import datetime

class JobPostCreate(BaseModel):
    title: str
    description: str

class JobPostResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True