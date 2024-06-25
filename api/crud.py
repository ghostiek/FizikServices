from sqlalchemy.orm import Session
from . import models, schemas


#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user: schemas.User):
    return (db.query(models.User)
            .filter(models.User.user_id == user.user_id)
            .filter(models.User.password == user.password)
            .first()
            )


def create_user(db: Session, user: schemas.User):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FoodLog).offset(skip).limit(limit).all()


def create_food_log(db: Session, item: schemas.FoodLog):
    db_item = models.FoodLog(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
