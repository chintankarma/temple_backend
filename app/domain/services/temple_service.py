from app.infrastructure.repositories.temple_repo import TempleRepository
from app.core.security import hash_password

class TempleService:

    @staticmethod
    def create_temple(db, data):
        hashed_password = hash_password(data.password)
        temple = TempleRepository.create_temple(db, data, hashed_password)
        return {"success": True, "message": "Temple created", "id": temple.id}

    @staticmethod
    def get_temple(db, temple_id: int):
        temple = TempleRepository.get_temple_by_id(db, temple_id)
        if not temple:
            return None
        return {
            "id": temple.id,
            "name": temple.name,
            "description": temple.description,
            "address": temple.address,
            "state": temple.state,
            "district": temple.district,
            "mobile_number": temple.mobile_number,
            "email": temple.email,
        }

    @staticmethod
    def get_temples(db):
        temples = TempleRepository.get_all_temples(db)
        return {
            "success": True,
            "data": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "address": t.address,
                    "state": t.state,
                    "district": t.district,
                    "mobile_number": t.mobile_number,
                    "email": t.email,
                }
                for t in temples
            ],
        }

    @staticmethod
    def update_temple(db, temple_id: int, data):
        temple = TempleRepository.get_temple_by_id(db, temple_id)
        if not temple:
            return None
        updated = TempleRepository.update_temple(db, temple, data)
        return {
            "success": True,
            "message": "Temple updated",
            "data": {
                "id": updated.id,
                "name": updated.name,
                "description": updated.description,
                "address": updated.address,
                "state": updated.state,
                "district": updated.district,
                "mobile_number": updated.mobile_number,
                "email": updated.email,
            },
        }

    @staticmethod
    def delete_temple(db, temple_id: int):
        temple = TempleRepository.get_temple_by_id(db, temple_id)
        if not temple:
            return None
        TempleRepository.delete_temple(db, temple)
        return {"success": True, "message": "Temple deleted"}
