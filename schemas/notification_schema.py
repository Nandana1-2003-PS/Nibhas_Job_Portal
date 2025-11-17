from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    message: str
    job_id: int | None
    user_id:int
    created_at: datetime

    class Config:
        from_attributes = True
