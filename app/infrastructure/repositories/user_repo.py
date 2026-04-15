from sqlalchemy.orm import Session
from app.domain.models import user
from app.domain.models.user import User
from app.core.security import hash_password

class UserRepository:

    @staticmethod
    def get_user_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_mobile(db, mobile_no: str):
        return db.query(User).filter(User.mobile_no == mobile_no).first()   

    @staticmethod
    def create_user(db, data):
        from app.core.security import hash_password

        user = User(
            title=data["title"],
            name=data["name"],
            mobile_no=data["mobile_no"],
            email=data["email"],
            password=hash_password(data["password"]),
            indian_citizen=data["indian_citizen"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            address=data["address"],
            state=data["state"],
            district=data["district"],
            country=data.get("country"),
            profile_pic=data["profile_pic"]
        )

        db.add(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(user)

        return user

    @staticmethod
    def update_user(db, user, data):
        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)
    
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(user)
    
        return user
    
    @staticmethod
    def get_user_by_id(db, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def delete_user_by_id(db, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        db.delete(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return user