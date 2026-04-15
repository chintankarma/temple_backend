from app.infrastructure.repositories.temple_repo import TempleRepository
from app.infrastructure.repositories.user_repo import UserRepository

class TempleService:

    @staticmethod
    def create_temple(db, data, current_user_email):
        user = UserRepository.get_user_by_email(db, current_user_email)

        if user.role != "temple":
            return {"success": False, "message": "Only temple can add temple"}

        temple = TempleRepository.create_temple(db, data, user.id)

        return {"success": True, "message": "Temple created"}

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
                    "district": t.district
                }
                for t in temples
            ]
        }