from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Rental, Book
from ..schemas import RentalCreate

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/")
def rent_book(rental: RentalCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == rental.book_id).first()
    if not book or book.is_rented:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    new_rental = Rental(user_id=rental.user_id, book_id=rental.book_id)
    book.is_rented = True
    db.add(new_rental)
    db.commit()
    return {"message": "Book rented successfully"}
