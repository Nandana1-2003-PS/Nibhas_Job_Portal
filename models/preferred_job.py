from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PreferredJob(Base):
    __tablename__ = "preferred_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200))
    location = Column(String(300))
    salary_expectation = Column(String(200))
    job_type = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="preferred_jobs")  