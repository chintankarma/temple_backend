import uuid
import os
import shutil
from app.core.response import success_response, error_response

from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AuthService:

    @staticmethod
    def check_user_exists(db, email: str = None, mobile_no: str = None):
        if not email and not mobile_no:
            return {"success": False, "message": "Provide email or mobile_no"}

        if email:
            user = UserRepository.get_user_by_email(db, email)
            if user:
                return success_response(message="User exists with this email", data={"exists": True})
            return success_response(message="No user found with this email", data={"exists": False})

        user = UserRepository.get_user_by_mobile(db, mobile_no)
        if user:
            return success_response(message="User exists with this phone number", data={"exists": True})
        return success_response(message="No user found with this phone number", data={"exists": False})

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
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "mobile_no": user.mobile_no,
                "indian_citizen": user.indian_citizen,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "state": user.state,
                "district": user.district,
                "profile_pic": user.profile_pic
            }
        }

    @staticmethod
    def signup_user(
        db,
        title, name, mobile_no, email, password,
        indian_citizen, gender, date_of_birth,
        address, state, district, country,
        profile_pic
    ):
        existing_user = UserRepository.get_user_by_email(db, email)

        if existing_user:
            return success_response(message="User already exists with this email", data={"exists": True})

        existing_mobile = UserRepository.get_user_by_mobile(db, mobile_no)

        if existing_mobile:
            return error_response(message="Mobile already registered")

        if indian_citizen:
            if not state or not district:
                return error_response(message="State and district are required for Indian citizens")
        else:
            if not country:
                return error_response(message="Country is required for non-Indian citizens")

        if profile_pic:
            if profile_pic.content_type not in ALLOWED_TYPES:
                return error_response(message="Invalid file type")

            filename = f"{uuid.uuid4()}_{profile_pic.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_pic.file, buffer)

            profile_pic_url = f"/uploads/{filename}"
        else:
            profile_pic_url = None

        user = UserRepository.create_user(
            db,
            {
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
                "profile_pic": profile_pic_url
            }
        )

        return {
            "success": True,
            "message": "User created successfully",
            "user": {"email": user.email}
        }

    @staticmethod
    def get_profile(db, email):
        user = UserRepository.get_user_by_email(db, email)

        if not user:
            return success_response(message="User not found", data={"exists": False})

        return {
            "success": True,
            "data": {
                "title": user.title,
                "name": user.name,
                "mobile_no": user.mobile_no,
                "email": user.email,
                "indian_citizen": user.indian_citizen,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "state": user.state,
                "district": user.district,
                "profile_pic": user.profile_pic
            }
        }

    @staticmethod
    def update_profile(db, email, data):
        user = UserRepository.get_user_by_email(db, email)

        if not user:
            return error_response(message="User not found")

        UserRepository.update_user(db, user, data)

        return success_response(message="Profile updated")

    @staticmethod
    def delete_user(db, user_id: int, current_email: str):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            return error_response(message="User not found")

        if user.email != current_email:
            return error_response(message="Not authorized")

        db.delete(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return success_response(message="Profile deleted")
