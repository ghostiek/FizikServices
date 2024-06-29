from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "Credentials"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    date_created = Column(DateTime)
    # items = relationship("Item", back_populates="owner")


class FoodLog(Base):
    __tablename__ = "FoodLog"

    food_log_entry_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Credentials.user_id"))
    food_id = Column(String)
    serving_size = Column(String)
    amount = Column(Integer)
    date_created = Column(DateTime)

    # owner = relationship("Credentials", back_populates="user_id")
