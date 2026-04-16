from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.core.security import get_current_user
from app.domain.services.user_service import UserService
from app.schemas.user_schema import LoginRequest

router = APIRouter()

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
        title,
        name,
        mobile_no,
        email,
        password,
        indian_citizen,
        gender,
        date_of_birth,
        address,
        state,
        district,
        country,
        profile_pic,
    )


@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    return UserService.login_user(db, data)


@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# ── Protected (user token required) — defined before /{user_id} ──────────────


@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.get_profile(db, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/update")
def update_profile(
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
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserService.update_profile(
        db,
        current_user,
        title,
        name,
        mobile_no,
        email,
        password,
        indian_citizen,
        gender,
        date_of_birth,
        address,
        state,
        district,
        country,
        profile_pic,
    )


@router.delete("/delete")
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
