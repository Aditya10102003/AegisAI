from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.core.config import settings

# SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# SessionLocal for database sessions
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()