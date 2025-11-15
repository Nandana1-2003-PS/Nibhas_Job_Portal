from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(1000), nullable=False)
    job_id = Column(Integer, ForeignKey("job_posts.id"))  
    created_at = Column(DateTime, default=datetime.utcnow)

    job_post = relationship("JobPost", back_populates="notifications")