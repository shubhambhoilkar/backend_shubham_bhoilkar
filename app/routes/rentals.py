from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Rental, Book
from ..schemas import RentalCreate, RentalResponse

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/", response_model=RentalResponse)
def rent_book(rental: RentalCreate, db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).filter(Book.id == rental.book_id, Book.available == True).first()
        if not db_book:
            raise HTTPException(status_code=400, detail="Book is not available")
        
        db_book.available = False
        new_rental = Rental(**rental.dict())
        db.add(new_rental)
        db.commit()
        db.refresh(new_rental)
        return new_rental
    except Exception as e:
        return f"Error occured at router while uploading book data.{e}"

@router.put("/{rental_id}/return")
def return_book(rental_id: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")
        
        rental.book.available = True
        rental.returned_at = datetime.datetime.utcnow()
        db.commit()
        return {"message": "Book returned successfully"}
    except Exception as e:
        return f"Eror occured at router, updating return book.{e}"