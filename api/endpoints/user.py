from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api import crud, models
from api.schemas import FoodLogSchema, UserSchema
from api.database import SessionLocal, engine

@app.post("/users/create", response_model=UserSchema.User)
async def create_user(user: UserSchema.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=UserSchema.User)
async def login_user(user: UserSchema.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    # Create JWT and send it back
    return

@app.get("/users/me")
async def read_users_me(current_user: Annotated[UserSchema.User, Depends(get_current_user)]):
    return current_user
