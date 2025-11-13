from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    message: str
    job_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
