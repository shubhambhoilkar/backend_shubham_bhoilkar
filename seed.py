from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Book
from app.auth import get_password_hash

db: Session = SessionLocal()

user1 = User(name="Alice", email="alice@example.com", password=get_password_hash("password123"))
book1 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald")

db.add_all([user1, book1])
db.commit()

print("Dummy data inserted successfully!")
