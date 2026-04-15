from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.database import Base

class Temple(Base):
    __tablename__ = "temples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    state = Column(String)
    district = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))