from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from ..schemas import BookCreate, BookResponse
import shutil
import os

router = APIRouter(prefix="/books", tags=["Books"])

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        new_book = Book(**book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        return f"An error occured while adding book. {e}"

@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    try:
        return db.query(Book).all()
    except Exception as e:
        return f"An error occured while geting book. {e}"

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        db_book.title = book.title
        db_book.author = book.author
        db.commit()
        return db_book
    except Exception as e:
        return f"An error occured during updating data. {e}"

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted"}
    except Exception as e:
        return f"an error occured during deleting the book. {e}"

@router.post("/{book_id}/upload_cover")
def upload_cover(book_id: int, file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "path": file_path}
    except Exception as e:
        return f"An errror occured during uploading the book cover.{e}"