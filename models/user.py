from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)

  
    education_details = relationship("EducationDetails", back_populates="user", cascade="all, delete-orphan")
    preferred_jobs = relationship("PreferredJob", back_populates="user", cascade="all, delete-orphan")
