from sqlalchemy import Column, Integer, String
from database import Base

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
