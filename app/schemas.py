from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_rented: bool

    class Config:
        orm_mode = True

class RentalCreate(BaseModel):
    user_id: int
    book_id: int

class RentalResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rented_at: datetime
    returned_at: Optional[datetime] = None
    class Config:
        from_attributes = True
