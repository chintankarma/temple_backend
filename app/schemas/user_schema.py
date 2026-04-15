from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from pydantic import Field

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
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

class UpdateProfileRequest(BaseModel):
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