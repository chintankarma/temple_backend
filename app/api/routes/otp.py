from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.otp_store import generate_otp, verify_otp
from app.core.deps import get_db
from app.core.security import create_access_token
from app.infrastructure.repositories.user_repo import UserRepository
from app.api_keyword import AppStrings

router = APIRouter()


@router.post("/send")
def send_otp(mobile_no: str, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_mobile(db, mobile_no)
    if not user:
        return {"success": False, "message": "No user found with this mobile number"}

    otp = generate_otp(mobile_no)
    return {
        "success": True,
        "message": "OTP sent",
        "otp": otp
    }


@router.post("/verify")
def verify(mobile_no: str, otp: str, db: Session = Depends(get_db)):
    if not verify_otp(mobile_no, otp):
        return {"success": False, "message": "Invalid OTP"}

    user = UserRepository.get_user_by_mobile(db, mobile_no)
    if not user:
        return {"success": False, "message": "User not found"}

    token = {
        AppStrings.tokenType: "bearer",
        AppStrings.accessToken: create_access_token({"sub": user.email})
    }

    return {
        "success": True,
        "message": "Login successful.",
        "token": token,
        "data": {
            AppStrings.id: user.id,
            AppStrings.title: user.title,
            AppStrings.name: user.name,
            AppStrings.mobileNo: user.mobile_no,
            AppStrings.email: user.email,
            AppStrings.indianCitizen: user.indian_citizen,
            AppStrings.gender: user.gender,
            AppStrings.dateOfBirth: user.date_of_birth,
            AppStrings.address: user.address,
            AppStrings.state: user.state,
            AppStrings.district: user.district,
            AppStrings.country: user.country,
            AppStrings.profilePic: user.profile_pic,
            AppStrings.role: user.role,
            AppStrings.createdAt: user.created_at.isoformat() if user.created_at else None,
            AppStrings.updatedAt: user.updated_at.isoformat() if user.updated_at else None,
        }
    }
