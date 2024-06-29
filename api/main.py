from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models
from api.schemas import FoodLogSchema, UserSchema, TokenSchema
from .crud import get_user
from .database import SessionLocal, engine
from api.security import PasswordContext
import jwt
from api.endpoints import *

pwd_context = PasswordContext.PasswordContext()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/items/", response_model=FoodLogSchema.FoodLog)
async def create_item_for_user(item: FoodLogSchema.FoodLog,
                               token: Annotated[str, Depends(oauth2_scheme)],
                               db: Session = Depends(get_db)
                               ):
    print(token)
    return crud.create_food_log(db=db, item=item)


@app.post("/users/create", response_model=UserSchema.UserInDB)
async def create_user(user: UserSchema.UserCreationInput, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=UserSchema.User)
async def login_user(user: UserSchema.User,
                     db: Session = Depends(get_db)
                     ):
    db_user = crud.get_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    # Create JWT and send it back
    return

@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
) -> TokenSchema.Token:
    user = UserSchema.UserInDB(username=form_data.username,
                               hashed_password=form_data.password)
    auth_user = crud.authenticate_user(db, user)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=pwd_context.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = pwd_context.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenSchema.Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)
                           ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, pwd_context.SECRET_KEY, algorithms=[pwd_context.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenSchema.TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(db, user=UserSchema.User(username=token_data.username))
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[UserSchema.User, Depends(get_current_user)]):
    return current_user
