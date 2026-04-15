from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.deps import get_db
from app.domain.services.temple_service import TempleService
from pydantic import BaseModel, EmailStr

router = APIRouter()


class TempleCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    mobile_number: str
    email: EmailStr
    password: str


class TempleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None


@router.post("/create")
def create_temple(data: TempleCreateRequest, db: Session = Depends(get_db)):
    return TempleService.create_temple(db, data)


@router.get("/all")
def get_temples(db: Session = Depends(get_db)):
    return TempleService.get_temples(db)


@router.get("/{temple_id}")
def get_temple(temple_id: int, db: Session = Depends(get_db)):
    temple = TempleService.get_temple(db, temple_id)
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")
    return {"success": True, "data": temple}


@router.put("/{temple_id}")
def update_temple(temple_id: int, data: TempleUpdateRequest, db: Session = Depends(get_db)):
    result = TempleService.update_temple(db, temple_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result


@router.delete("/{temple_id}")
def delete_temple(temple_id: int, db: Session = Depends(get_db)):
    result = TempleService.delete_temple(db, temple_id)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result
