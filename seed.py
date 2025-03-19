from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Book
from app.auth import get_password_hash

db: Session = SessionLocal()

user1 = User(name="Shubham", email="shubhambhoilkar@gmail.com", password=get_password_hash("sam@9601"))
book1 = Book(title="REWORK", author="Jason Fried and David Heinemeier Hansson ")

db.add_all([user1, book1])
db.commit()

print("Book Data Inserted Successfully!")
