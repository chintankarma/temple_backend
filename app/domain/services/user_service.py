import uuid
import os
import shutil

from app.api_keyword import AppStrings
from app.response_model import BaseApiResponse
from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _user_dict(u):
    return {
        AppStrings.id: u.id,
        AppStrings.title: u.title,
        AppStrings.name: u.name,
        AppStrings.mobileNo: u.mobile_no,
        AppStrings.email: u.email,
        AppStrings.indianCitizen: u.indian_citizen,
        AppStrings.gender: u.gender,
        AppStrings.dateOfBirth: u.date_of_birth,
        AppStrings.address: u.address,
        AppStrings.state: u.state,
        AppStrings.district: u.district,
        AppStrings.country: u.country,
        AppStrings.profilePic: u.profile_pic,
        AppStrings.role: u.role,
        AppStrings.createdAt: u.created_at.isoformat() if u.created_at else None,
        AppStrings.updatedAt: u.updated_at.isoformat() if u.updated_at else None,
    }


class UserService:

    @staticmethod
    def register_user(
        db,
        title, name, mobile_no, email, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, country,
        profile_pic,
    ):
        if UserRepository.get_user_by_email(db, email):
            return BaseApiResponse(success=False, message="User already registered with this email")

        if UserRepository.get_user_by_mobile(db, mobile_no):
            return BaseApiResponse(success=False, message="User already registered with this mobile number")

        if indian_citizen:
            if not state or not district:
                return BaseApiResponse(success=False, message="State and district are required for Indian citizens")
        else:
            if not country:
                return BaseApiResponse(success=False, message="Country is required for non-Indian citizens")

        profile_pic_url = None
        if profile_pic:
            filename = f"{uuid.uuid4()}_{profile_pic.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_pic.file, buffer)
            profile_pic_url = f"/uploads/{filename}"

        user = UserRepository.create_user(db, {
            "title": title,
            "name": name,
            "mobile_no": mobile_no,
            "email": email,
            "password": password,
            "indian_citizen": indian_citizen,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "address": address,
            "state": state,
            "district": district,
            "country": country,
            "profile_pic": profile_pic_url,
        })

        return BaseApiResponse(success=True, message="User registered successfully", data=_user_dict(user))

    @staticmethod
    def login_user(db, data):
        user = UserRepository.get_user_by_email(db, data.email)
        if not user:
            return BaseApiResponse(success=False, message="User not found")

        if not verify_password(data.password, user.password):
            return BaseApiResponse(success=False, message="Wrong password")
        
        token = {
            "token_type": "bearer",
            "access_token": create_access_token({"sub": user.email})
        }

        
        return BaseApiResponse(
            success=True,
            message="Login successful",
            token=token,
            data=_user_dict(user)
        )

    @staticmethod
    def get_all_users(db):
        users = UserRepository.get_all_users(db)
        return BaseApiResponse(success=True, message="Users retrieved successfully", data=[_user_dict(u) for u in users])

    @staticmethod
    def get_user(db, user_id: int):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return BaseApiResponse(success=False, message="User not found")
        return BaseApiResponse(success=True, message="User retrieved successfully", data=_user_dict(user))

    @staticmethod
    def get_profile(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return BaseApiResponse(success=False, message="User not found")
        return BaseApiResponse(success=True, message="Profile retrieved successfully", data=_user_dict(user))

    @staticmethod
    def update_profile(
        db,
        email,
        title, name, mobile_no, email_new, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, country,
        profile_pic,
    ):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return BaseApiResponse(success=False, message="User not found")

        if email_new != email and UserRepository.get_user_by_email(db, email_new):
            return BaseApiResponse(success=False, message="User already registered with this email")

        if mobile_no != user.mobile_no and UserRepository.get_user_by_mobile(db, mobile_no):
            return BaseApiResponse(success=False, message="User already registered with this mobile number")

        if indian_citizen:
            if not state or not district:
                return BaseApiResponse(success=False, message="State and district are required for Indian citizens")
        else:
            if not country:
                return BaseApiResponse(success=False, message="Country is required for non-Indian citizens")

        profile_pic_url = None
        if profile_pic:
            filename = f"{uuid.uuid4()}_{profile_pic.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_pic.file, buffer)
            profile_pic_url = f"/uploads/{filename}"

        updated = UserRepository.update_user(db, user, {
            "title": title,
            "name": name,
            "mobile_no": mobile_no,
            "email": email_new,
            "password": password,
            "indian_citizen": indian_citizen,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "address": address,
            "state": state,
            "district": district,
            "country": country,
            "profile_pic": profile_pic_url,
        })
        return BaseApiResponse(success=True, message="Profile updated", data=_user_dict(updated))

    @staticmethod
    def delete_user(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return BaseApiResponse(success=False, message="User not found")
        UserRepository.delete_user(db, user)
        return BaseApiResponse(success=True, message="User deleted")
