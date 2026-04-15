from fastapi import APIRouter
from app.core.otp_store import generate_otp, verify_otp

router = APIRouter()

@router.post("/send")
def send_otp(mobile_no: str):
    otp = generate_otp(mobile_no)

    # 🔥 For now we return OTP (later SMS)
    return {
        "success": True,
        "message": "OTP sent",
        "otp": otp
    }


@router.post("/verify")
def verify(mobile_no: str, otp: str):
    if verify_otp(mobile_no, otp):
        return {"success": True, "message": "OTP verified"}

    return {"success": False, "message": "Invalid OTP"}