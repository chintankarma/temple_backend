from pydantic import EmailStr, Field
from typing import Optional
from pydantic import Field

from app.response_model import CleanBaseModel

class LoginRequest(CleanBaseModel):
    email: str
    password: str

class SignupRequest(CleanBaseModel):
    title: str
    name: str
    mobile_no: str
    email: EmailStr
    password: str = Field(min_length=6)
    indian_citizen: bool
    gender: str
    date_of_birth: str
    address: str
    state: str
    district: str
    profile_pic: Optional[str] = None

class UpdateProfileRequest(CleanBaseModel):
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
    profile_pic: Optional[str] = None