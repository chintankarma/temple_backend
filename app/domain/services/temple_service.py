from app.infrastructure.repositories.temple_repo import TempleRepository

class TempleService:

    @staticmethod
    def create_temple(db, data):
        TempleRepository.create_temple(db, data, user_id=None)
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