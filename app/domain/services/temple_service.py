from app.infrastructure.repositories.temple_repo import TempleRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.response import success_response, error_response


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
            return error_response(message="Temple already registered with this email")

        existing_mobile = TempleRepository.get_temple_by_mobile(db, data.mobile_number)
        if existing_mobile:
            return error_response(message="Temple already registered with this mobile number")

        hashed = hash_password(data.password)
        temple = TempleRepository.create_temple(db, data, hashed)
        return success_response(message="Temple registered successfully", data={"id": temple.id})

    @staticmethod
    def login_temple(db, data):
        temple = TempleRepository.get_temple_by_email(db, data.email)
        if not temple:
            return error_response(message="Temple not found")

        if not verify_password(data.password, temple.password):
            return error_response(message="Wrong password")

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
            return error_response(message="Temple not found")
        return success_response(data=_temple_dict(temple))

    @staticmethod
    def get_temple(db, temple_id: int):
        temple = TempleRepository.get_temple_by_id(db, temple_id)
        if not temple:
            return error_response(message="Temple not found")
        return success_response(data=_temple_dict(temple))

    @staticmethod
    def get_temples(db):
        temples = TempleRepository.get_all_temples(db)
        return success_response(data=[_temple_dict(t) for t in temples])

    @staticmethod
    def update_temple(db, current_email: str, data):
        temple = TempleRepository.get_temple_by_email(db, current_email)
        if not temple:
            return error_response(message="Temple not found")
        updated = TempleRepository.update_temple(db, temple, data)
        return success_response(message="Temple updated", data=_temple_dict(updated))

    @staticmethod
    def delete_temple(db, current_email: str):
        temple = TempleRepository.get_temple_by_email(db, current_email)
        if not temple:
            return error_response(message="Temple not found")
        TempleRepository.delete_temple(db, temple)
        return success_response(message="Temple deleted")
