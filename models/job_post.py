from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    vacancies = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    admin_id = Column(Integer, ForeignKey("admins.id"))
    admin = relationship("Admin", back_populates="job_posts")

    notifications = relationship("Notification", back_populates="job_post", cascade="all, delete")