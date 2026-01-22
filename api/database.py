from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Database URL configuration
# SQLite for development, can be changed to PostgreSQL, MySQL, etc.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./company_agents.db"
)

# Engine configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    )
else:
    # PostgreSQL and other databases
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session.
    
    Usage in routes:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


def init_db():
    """
    Initialize database tables.
    
    This should be called once during application startup.
    """
    from database.models import Base
    Base.metadata. create_all(bind=engine)


def drop_all_tables():
    """
    Drop all tables from database.
    
    WARNING: This will delete all data!  Use only for development/testing.
    """
    from database.models import Base
    Base.metadata.drop_all(bind=engine)


def reset_db():
    """
    Reset database by dropping all tables and recreating them. 
    
    WARNING: This will delete all data! Use only for development/testing.
    """
    drop_all_tables()
    init_db()