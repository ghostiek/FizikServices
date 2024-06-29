from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Union[str, None] = None
    date_created: Optional[datetime] = Field(default=datetime.now())

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class UserCreationInput(User):
    password: str
