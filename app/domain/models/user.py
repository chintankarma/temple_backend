from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.infrastructure.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    name = Column(String)
    mobile_no = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    indian_citizen = Column(Boolean)
    gender = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    state = Column(String)
    district = Column(String)
    country = Column(String)
    profile_pic = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))