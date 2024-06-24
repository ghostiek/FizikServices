from datetime import datetime
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
