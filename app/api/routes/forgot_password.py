from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.deps import get_db
from app.core.otp_store import generate_otp, verify_otp
from app.core.security import hash_password
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.repositories.temple_repo import TempleRepository

router = APIRouter()


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    role: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    role: str
    otp: str
    new_password: str


def _get_account(db, email: str, role: str):
    role = role.lower()
    if role == "user":
        return UserRepository.get_user_by_email(db, email)
    elif role == "temple":
        return TempleRepository.get_temple_by_email(db, email)
    return None


@router.post("/request")
def request_otp(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    if data.role.lower() not in ("user", "temple"):
        return {"success": False, "message": "Invalid role. Must be 'user' or 'temple'"}

    account = _get_account(db, data.email, data.role)
    if not account:
        return {"success": False, "message": f"No {data.role} found with this email"}

    otp = generate_otp(data.email)

    return {
        "success": True,
        "message": f"OTP sent to {data.email}",
        "otp": otp,
    }


@router.post("/reset")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if data.role.lower() not in ("user", "temple"):
        return {"success": False, "message": "Invalid role. Must be 'user' or 'temple'"}

    if not verify_otp(data.email, data.otp):
        return {"success": False, "message": "Invalid or expired OTP"}

    account = _get_account(db, data.email, data.role)
    if not account:
        return {"success": False, "message": f"No {data.role} found with this email"}

    account.password = hash_password(data.new_password)
    db.commit()

    return {"success": True, "message": "Password reset successfully"}
