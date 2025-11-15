from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class PersonalDetails(Base):
    __tablename__ = "personal_details"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    phone = Column(String(200))
    date_of_birth = Column(String(200))
    address = Column(String(500))
    city = Column(String(200))
    state = Column(String(200))
    pincode = Column(String(200))