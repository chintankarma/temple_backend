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


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


def _find_account(db, email: str):
    user = UserRepository.get_user_by_email(db, email)
    if user:
        return user, "user"
    temple = TempleRepository.get_temple_by_email(db, email)
    if temple:
        return temple, "temple"
    return None, None


@router.post("/request")
def request_otp(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    account, role = _find_account(db, data.email)
    if not account:
        return {"success": False, "message": "No account found with this email"}

    otp = generate_otp(data.email)
    return {
        "success": True,
        "message": f"OTP sent to {data.email}",
        "role": role,
        "otp": otp,
    }


@router.post("/reset")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not verify_otp(data.email, data.otp):
        return {"success": False, "message": "Invalid or expired OTP"}

    account, role = _find_account(db, data.email)
    if not account:
        return {"success": False, "message": "No account found with this email"}

    account.password = hash_password(data.new_password)
    db.commit()

    return {"success": True, "message": f"{role.capitalize()} password reset successfully"}
