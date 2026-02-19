from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, crud
from ..utils.logger import logger
router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user with email: {user.email}")
    print("USER CREATE PAYLOAD:", user)
    return crud.create_user(db, user)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

