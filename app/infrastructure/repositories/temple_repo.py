from app.domain.models.temple import Temple

class TempleRepository:

    @staticmethod
    def create_temple(db, data, owner_id):
        temple = Temple(
            name=data.name,
            description=data.description,
            address=data.address,
            state=data.state,
            district=data.district,
            owner_id=owner_id
        )

        db.add(temple)
        db.commit()
        db.refresh(temple)

        return temple

    @staticmethod
    def get_all_temples(db):
        return db.query(Temple).all()