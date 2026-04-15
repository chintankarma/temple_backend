from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import get_current_user
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
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return TempleService.create_temple(db, data, current_user)


@router.get("/all")
def get_temples(db: Session = Depends(get_db)):
    return TempleService.get_temples(db)