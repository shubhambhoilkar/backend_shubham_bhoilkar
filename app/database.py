from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the DATABASE_URL for MySQL
DATABASE_URL = "mysql+mysqlconnector://root:Sam@99@localhost/book_rental"

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
