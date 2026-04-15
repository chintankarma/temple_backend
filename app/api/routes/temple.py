from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.domain.services.temple_service import TempleService
from pydantic import BaseModel

router = APIRouter()

class TempleRequest(BaseModel):
    name: str
    description: str
    address: str
    state: str
    district: str


@router.post("/create")
def create_temple(
    data: TempleRequest,
    db: Session = Depends(get_db)
):
    return TempleService.create_temple(db, data)


@router.get("/all")
def get_temples(db: Session = Depends(get_db)):
    return TempleService.get_temples(db)