from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.core.deps import get_db
from app.core.security import get_current_user
from app.domain.services.user_service import UserService

router = APIRouter()


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    indian_citizen: Optional[bool] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    country: Optional[str] = None


# ── Public ───────────────────────────────────────────────────────────────────

@router.post("/register")
def register_user(
    title: str = Form(...),
    name: str = Form(...),
    mobile_no: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    indian_citizen: bool = Form(...),
    gender: str = Form(...),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    profile_pic: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return UserService.register_user(
        db,
        title, name, mobile_no, email, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, country,
        profile_pic,
    )


@router.post("/login")
def login_user(data: UserLoginRequest, db: Session = Depends(get_db)):
    return UserService.login_user(db, data)


@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# ── Protected (user token required) — defined before /{user_id} ──────────────

@router.get("/auth/me")
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.get_profile(db, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/auth/update")
def update_profile(
    data: UserUpdateRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.update_profile(db, current_user, data)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.delete("/auth/delete")
def delete_user(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.delete_user(db, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


# ── Public — dynamic route last ───────────────────────────────────────────────

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = UserService.get_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
