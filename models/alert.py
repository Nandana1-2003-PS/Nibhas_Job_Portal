from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
