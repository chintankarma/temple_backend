import uuid
import os
import shutil

from app.api_keyword import AppStrings
from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.image_helper import save_image

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
            return {"success": False, "message": "User already registered with this email"}

        if UserRepository.get_user_by_mobile(db, mobile_no):
            return {"success": False, "message": "User already registered with this mobile number"}

        if indian_citizen:
            if not state or not district:
                return {"success": False, "message": "State and district are required for Indian citizens"}
        else:
            if not country:
                return {"success": False, "message": "Country is required for non-Indian citizens"}

        profile_pic_url = None
        if profile_pic and getattr(profile_pic, "filename", None):
            profile_pic_url, error = save_image(profile_pic)

            if error:
                return {"success": False, "message": error}

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

        token = {
            AppStrings.tokenType: "bearer",
            AppStrings.accessToken: create_access_token({"sub": user.email})
        }

        return {"success": True, "message": "User registered successfully", "token": token, "data": _user_dict(user)}

    @staticmethod
    def login_user(db, data):
        user = UserRepository.get_user_by_email(db, data.email)
        if not user:
            return {"success": False, "message": "User not found"}

        if not verify_password(data.password, user.password):
            return {"success": False, "message": "Wrong password"}
        
        token = {
            AppStrings.tokenType: "bearer",
            AppStrings.accessToken: create_access_token({"sub": user.email})
        }

        
        return {"success": True, "message": "Login successful", "token": token, "data": _user_dict(user)}

    @staticmethod
    def get_all_users(db):
        users = UserRepository.get_all_users(db)
        return {"success": True, "message": "Users retrieved successfully", "data": [_user_dict(u) for u in users]} 

    @staticmethod
    def get_user(db, user_id: int):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return {"success": False, "message": "User not found"}
        return {"success": True, "message": "User retrieved successfully", "data": _user_dict(user)}

    @staticmethod
    def get_profile(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return {"success": False, "message": "User not found"}
        return {"success": True, "message": "Profile retrieved successfully", "data": _user_dict(user)}

    @staticmethod
    def update_profile(db, email, **data):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return {"success": False, "message": "User not found"}

        # ✅ Email uniqueness
        if "email" in data and data["email"] != email:
            if UserRepository.get_user_by_email(db, data["email"]):
                return {"success": False, "message": "Email already exists"}

        # ✅ Mobile uniqueness
        if "mobile_no" in data and data["mobile_no"] != user.mobile_no:
            if UserRepository.get_user_by_mobile(db, data["mobile_no"]):
                return {"success": False, "message": "Mobile already exists"}

        # ✅ Indian validation
        if "indian_citizen" in data:
            if data["indian_citizen"]:
                if not data.get("state") or not data.get("district"):
                    return {"success": False, "message": "State & district required"}
            else:
                if not data.get("country"):
                    return {"success": False, "message": "Country required"}

        # ✅ Delete old image if new one comes
        if "profile_pic" in data and user.profile_pic:
            old_filename = user.profile_pic.split("/")[-1]
            old_path = os.path.join(UPLOAD_DIR, old_filename)

            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception:
                    pass

        # ✅ Build update data
        update_data = {}

        for key, value in data.items():
            if value is not None:
                if key == "password":
                    update_data[key] = hash_password(value)
                else:
                    update_data[key] = value

        updated = UserRepository.update_user(db, user, update_data)

        return {
            "success": True,
            "message": "Profile updated",
            "data": _user_dict(updated)
        }
    
    @staticmethod
    def delete_profile_pic(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return {"success": False, "message": "User not found"}
        if user.profile_pic:
            old_path = os.path.join(UPLOAD_DIR, user.profile_pic.split('/')[-1])
            if os.path.exists(old_path):
                os.remove(old_path)
            UserRepository.update_user(db, user, {"profile_pic": None})
        return {"success": True, "message": "Profile picture deleted"}

    @staticmethod
    def delete_user(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return {"success": False, "message": "User not found"}
        UserRepository.delete_user(db, user)
        return {"success": True, "message": "User deleted"}
