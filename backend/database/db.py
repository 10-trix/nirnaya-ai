import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get Database URL from environment variable or default to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/nirnaya_db")

# Create engine with fallback to SQLite if PostgreSQL fails to connect or is unavailable
try:
    if DATABASE_URL.startswith("postgresql"):
        # Test postgres engine creation
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        # Try a quick connection test
        with engine.connect() as conn:
            pass
    else:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
except Exception:
    # Fallback to local SQLite database for development/testing if PostgreSQL is not active
    SQLITE_URL = "sqlite:///./nirnaya.db"
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
