from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PreferredJob(Base):
    __tablename__ = "preferred_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    location = Column(String)
    salary_expectation = Column(String)
    job_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))




