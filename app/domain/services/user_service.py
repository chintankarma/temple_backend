import uuid
import os
import shutil
from datetime import timedelta
import cloudinary.uploader

from app.api_keyword import AppStrings
from app.infrastructure.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.image_helper import save_image

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
            try:
                result = cloudinary.uploader.upload(profile_pic.file)
                profile_pic_url = result.get("secure_url")
            except Exception as e:
                return {"success": False, "message": str(e)}

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
    def update_profile(db, current_email, **data):
        user = UserRepository.get_user_by_email(db, current_email)
        if not user:
            return {"success": False, "message": "User not found"}
        
        # ✅ Handle email update
        new_email = data.get("email")

        if new_email and new_email != current_email:
            existing = UserRepository.get_user_by_email(db, new_email)
            if existing:
                return {"success": False, "message": "Email already exists"}

            user.email = new_email  # update email

        # ❌ Remove email from further processing
        data.pop("email", None)

        # ✅ Detect final citizenship (new OR existing)
        final_citizen = data.get("indian_citizen", user.indian_citizen)

        # ✅ Only validate if citizenship is actually changed
        if "indian_citizen" in data and data["indian_citizen"] != user.indian_citizen:
            if final_citizen:
                if not data.get("state"):
                    return {"success": False, "message": "State required"}
                if not data.get("district"):
                    return {"success": False, "message": "District required"}
            else:
                if not data.get("country"):
                    return {"success": False, "message": "Country required"}

        if "profile_pic" in data and data["profile_pic"]:
            try:
                result = cloudinary.uploader.upload(data["profile_pic"].file)
                data["profile_pic"] = result.get("secure_url")
            except Exception as e:
                return {"success": False, "message": str(e)}

        # ✅ Update data
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
            try:
                public_id = user.profile_pic.split("/")[-1]
                public_id = public_id.split(".")[0]
                cloudinary.uploader.destroy(public_id)
            except Exception:
                pass
            UserRepository.update_user(db, user, {"profile_pic": None})
        return {"success": True, "message": "Profile picture deleted"}

    @staticmethod
    def delete_user(db, email: str):
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            return {"success": False, "message": "User not found"}
        UserRepository.delete_user(db, user)
        return {"success": True, "message": "User deleted"}
