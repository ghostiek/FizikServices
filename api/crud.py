from sqlalchemy.orm import Session
from . import models
from api.schemas import FoodLogSchema, UserSchema


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, user: UserSchema.UserInDB):
    return (db.query(models.User)
            .filter(models.User.username == user.username)
            .filter(models.User.hashed_password == user.hashed_password)
            .first()
            )


def get_user(db: Session, user: UserSchema.User):
    return (db.query(models.User)
            .filter(models.User.username == user.username)
            .first()
            )


def create_user(db: Session,
                user: UserSchema.UserCreationInput):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FoodLog).offset(skip).limit(limit).all()


def create_food_log(db: Session, item: FoodLogSchema.FoodLog):
    db_item = models.FoodLog(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
