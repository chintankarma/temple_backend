from app.domain.models.temple import Temple

class TempleRepository:

    @staticmethod
    def create_temple(db, data, hashed_password: str):
        temple = Temple(
            name=data.name,
            description=data.description,
            address=data.address,
            state=data.state,
            district=data.district,
            mobile_number=data.mobile_number,
            email=data.email,
            password=hashed_password,
        )
        db.add(temple)
        db.commit()
        db.refresh(temple)
        return temple

    @staticmethod
    def get_temple_by_id(db, temple_id: int):
        return db.query(Temple).filter(Temple.id == temple_id).first()

    @staticmethod
    def get_temple_by_email(db, email: str):
        return db.query(Temple).filter(Temple.email == email).first()

    @staticmethod
    def get_temple_by_mobile(db, mobile_number: str):
        return db.query(Temple).filter(Temple.mobile_number == mobile_number).first()

    @staticmethod
    def get_all_temples(db):
        return db.query(Temple).all()

    @staticmethod
    def update_temple(db, temple: Temple, data):
        update_fields = data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(temple, field, value)
        db.commit()
        db.refresh(temple)
        return temple

    @staticmethod
    def delete_temple(db, temple: Temple):
        db.delete(temple)
        db.commit()
