from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class PersonalDetails(Base):
    __tablename__ = "personal_details"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)