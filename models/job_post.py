from sqlalchemy import Column, Integer, String, Text
from database import Base

class JobPost(Base):
    __tablename__ = "job_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    salary = Column(String)
    job_type = Column(String)