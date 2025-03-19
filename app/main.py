from fastapi import FastAPI
from .database import engine, Base
from .routes import users, books, rentals

# Initialize FastAPI app
app = FastAPI(title="Book Rental System", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(rentals.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Book Rental System API"}
