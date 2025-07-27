from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base
from . import models

# Test database URL - using SQLite in-memory for faster tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def create_test_database():
    """Create all tables for testing"""
    Base.metadata.create_all(bind=engine)