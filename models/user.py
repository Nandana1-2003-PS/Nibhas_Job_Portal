from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.user_skill import user_skill



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    educations = relationship("EducationDetails", back_populates="user")
    skills = relationship("Skill", secondary=user_skill, backref="users")