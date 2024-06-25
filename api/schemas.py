from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    date_created: Optional[datetime] = Field(default=datetime.now())

    class Config:
        orm_mode = True


class FoodLog(BaseModel):
    food_log_entry_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    food_id: int
    serving_size: str
    amount: str
    date_created: Optional[datetime] = Field(default=datetime.now(timezone.utc))

    class Config:
        orm_mode = True
