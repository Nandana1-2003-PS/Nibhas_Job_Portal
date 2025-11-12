from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class EmployerJob(Base):
    __tablename__ = "employer_jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary = Column(String)
    job_type = Column(String)
    vacancy=Column(Integer)
    employer_id = Column(Integer, ForeignKey("employers.id"))
