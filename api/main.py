from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.post("/users/create", response_model=schemas.User)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=schemas.User)
async def login_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    # Create JWT and send it back
    return


@app.post("/users/items/", response_model=schemas.FoodLog)
async def create_item_for_user(item: schemas.FoodLog, db: Session = Depends(get_db)):
    return crud.create_food_log(db=db, item=item)
