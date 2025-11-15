from sqlalchemy import Column, Integer, String
from database import Base

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(150), unique=True)
    password_hash = Column(String(255), nullable=False)
