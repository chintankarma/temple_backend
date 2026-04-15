from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base

class Temple(Base):
    __tablename__ = "temples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    state = Column(String)
    district = Column(String)
    mobile_number = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
