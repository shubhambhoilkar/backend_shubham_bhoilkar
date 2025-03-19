from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..utils import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
