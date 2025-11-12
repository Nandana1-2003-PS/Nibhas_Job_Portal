# models/user_skill.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from database import Base

user_skill = Table(
    'user_skill',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)