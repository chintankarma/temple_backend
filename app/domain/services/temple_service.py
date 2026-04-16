from app.response_model import BaseApiResponse
from app.infrastructure.repositories.temple_repo import TempleRepository
from app.core.security import hash_password, verify_password, create_access_token


def _temple_dict(t, include_id=True):
    d = {
        "name": t.name,
        "description": t.description,
        "address": t.address,
        "state": t.state,
        "district": t.district,
        "mobile_number": t.mobile_number,
        "email": t.email,
    }
    if include_id:
        d["id"] = t.id
    return d


class TempleService:

    @staticmethod
    def create_temple(db, data):
        existing = TempleRepository.get_temple_by_email(db, data.email)
        if existing:
            return BaseApiResponse(success=False, message="Temple already registered with this email")

        existing_mobile = TempleRepository.get_temple_by_mobile(db, data.mobile_number)
        if existing_mobile:
            return BaseApiResponse(success=False, message="Temple already registered with this mobile number")

        hashed = hash_password(data.password)
        temple = TempleRepository.create_temple(db, data, hashed)
        return BaseApiResponse(success=True, message="Temple registered successfully", data={"id": temple.id})

    @staticmethod
    def login_temple(db, data):
        temple = TempleRepository.get_temple_by_email(db, data.email)
        if not temple:
            return BaseApiResponse(success=False, message="Temple not found")

        if not verify_password(data.password, temple.password):
            return BaseApiResponse(success=False, message="Wrong password")

        token = create_access_token({"temple_sub": temple.email})
        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "temple": _temple_dict(temple),
        }

    @staticmethod
    def get_temple_profile(db, email: str):
        temple = TempleRepository.get_temple_by_email(db, email)
        if not temple:
            return BaseApiResponse(success=False, message="Temple not found")
        return BaseApiResponse(success=True, data=_temple_dict(temple))

    @staticmethod
    def get_temple(db, temple_id: int):
        temple = TempleRepository.get_temple_by_id(db, temple_id)
        if not temple:
            return BaseApiResponse(success=False, message="Temple not found")
        return BaseApiResponse(success=True, data=_temple_dict(temple))

    @staticmethod
    def get_temples(db):
        temples = TempleRepository.get_all_temples(db)
        return BaseApiResponse(success=True, data=[_temple_dict(t) for t in temples])

    @staticmethod
    def update_temple(db, current_email: str, data):
        temple = TempleRepository.get_temple_by_email(db, current_email)
        if not temple:
            return BaseApiResponse(success=False, message="Temple not found")
        updated = TempleRepository.update_temple(db, temple, data)
        return BaseApiResponse(success=True, message="Temple updated", data=_temple_dict(updated))

    @staticmethod
    def delete_temple(db, current_email: str):
        temple = TempleRepository.get_temple_by_email(db, current_email)
        if not temple:
            return BaseApiResponse(success=False, message="Temple not found")
        TempleRepository.delete_temple(db, temple)
        return BaseApiResponse(success=True, message="Temple deleted")
