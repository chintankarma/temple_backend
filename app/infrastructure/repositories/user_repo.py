from app.domain.models.user_model import User
from app.core.security import hash_password


class UserRepository:

    @staticmethod
    def get_user_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_mobile(db, mobile_no: str):
        return db.query(User).filter(User.mobile_no == mobile_no).first()

    @staticmethod
    def get_user_by_id(db, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db):
        return db.query(User).all()

    @staticmethod
    def create_user(db, data: dict):
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
            state=data.get("state"),
            district=data.get("district"),
            country=data.get("country"),
            profile_pic=data.get("profile_pic"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db, user: User, data: dict):
        for field, value in data.items():
            if field == "password":
                setattr(user, field, hash_password(value))
            else:
                setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db, user: User):
        db.delete(user)
        db.commit()
