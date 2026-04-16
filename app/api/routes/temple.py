from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.deps import get_db
from app.core.security import get_current_temple
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


class TempleLoginRequest(BaseModel):
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


# ── Public ──────────────────────────────────────────────────────────────────

@router.post("/register")
def register_temple(data: TempleCreateRequest, db: Session = Depends(get_db)):
    return TempleService.create_temple(db, data)


@router.post("/login")
def login_temple(data: TempleLoginRequest, db: Session = Depends(get_db)):
    return TempleService.login_temple(db, data)


@router.get("/all")
def get_temples(db: Session = Depends(get_db)):
    return TempleService.get_temples(db)


@router.get("/{temple_id}")
def get_temple(temple_id: int, db: Session = Depends(get_db)):
    result = TempleService.get_temple(db, temple_id)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result


# ── Protected (temple token required) ───────────────────────────────────────

@router.get("/me")
def get_temple_me(
    current_temple: str = Depends(get_current_temple),
    db: Session = Depends(get_db),
):
    result = TempleService.get_temple_profile(db, current_temple)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result


@router.put("/update")
def update_temple(
    data: TempleUpdateRequest,
    current_temple: str = Depends(get_current_temple),
    db: Session = Depends(get_db),
):
    result = TempleService.update_temple(db, current_temple, data)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result


@router.delete("/delete")
def delete_temple(
    current_temple: str = Depends(get_current_temple),
    db: Session = Depends(get_db),
):
    result = TempleService.delete_temple(db, current_temple)
    if not result:
        raise HTTPException(status_code=404, detail="Temple not found")
    return result
