import uuid
import os
import shutil

from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.response import success_response, error_response

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _user_dict(u):
    return {
        "id": u.id,
        "title": u.title,
        "name": u.name,
        "mobile_no": u.mobile_no,
        "email": u.email,
        "indian_citizen": u.indian_citizen,
        "gender": u.gender,
        "date_of_birth": u.date_of_birth,
        "address": u.address,
        "state": u.state,
        "district": u.district,
        "country": u.country,
        "profile_pic": u.profile_pic,
        "role": u.role,
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
            return error_response(message="User already registered with this email")

        if UserRepository.get_user_by_mobile(db, mobile_no):
            return error_response(message="User already registered with this mobile number")

        if indian_citizen:
            if not state or not district:
                return error_response(message="State and district are required for Indian citizens")
        else:
            if not country:
                return error_response(message="Country is required for non-Indian citizens")

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

        return {"success": True, "message": "User registered successfully", "id": user.id}

    @staticmethod
    def login_user(db, data):
        user = UserRepository.get_user_by_email(db, data.email)
        if not user:
            return error_response(message="User not found")

        if not verify_password(data.password, user.password):
            return error_response(message="Wrong password")

        token = create_access_token({"sub": user.email})
        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": _user_dict(user),
        }

    @staticmethod
    def get_all_users(db):
        users = UserRepository.get_all_users(db)
        return success_response(data=[_user_dict(u) for u in users])

    @staticmethod
    def get_user(db, user_id: int):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return error_response(message="User not found")
        return success_response(data=_user_dict(user))

    @staticmethod
    def get_profile(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return error_response(message="User not found")
        return success_response(data=_user_dict(user))

    @staticmethod
    def update_profile(db, email: str, data):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return error_response(message="User not found")
        updated = UserRepository.update_user(db, user, data)
        return success_response(message="Profile updated", data=_user_dict(updated))

    @staticmethod
    def delete_user(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return error_response(message="User not found")
        UserRepository.delete_user(db, user)
        return success_response(message="User deleted")
