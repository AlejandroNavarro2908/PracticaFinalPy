import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app123@db:5432/appdb")

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
