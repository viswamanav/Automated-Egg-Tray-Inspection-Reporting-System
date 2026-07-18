from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import DATABASE_URL

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database tables
Base = declarative_base()