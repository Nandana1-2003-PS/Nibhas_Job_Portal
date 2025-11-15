from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class EmployerJob(Base):
    __tablename__ = "employer_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(200), nullable=False)
    salary = Column(String(200))
    job_type = Column(String(200))
    vaccancy=Column(Integer)
    employer_id = Column(Integer, ForeignKey("employers.id"))
