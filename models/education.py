from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EducationDetails(Base):
    __tablename__ = "education_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    qualification = Column(String)
    institution = Column(String)
    year_of_passing = Column(String)

    
    user = relationship("User", back_populates="educations")
