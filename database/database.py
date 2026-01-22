"""
Database Configuration and Session Management

Provides SQLAlchemy engine, session factory, and database utility functions
for the Company Agents system. Supports both SQLite (default) and PostgreSQL.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Import Base from models to avoid circular imports
from database.models import Base


# ============ DATABASE CONFIGURATION ============

# Get database URL from environment variable, default to SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./company_agents.db"
)

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL query logging
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Maximum overflow connections
        echo=False  # Set to True for SQL query logging
    )


# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============ DATABASE DEPENDENCIES ============

def get_db() -> Generator:
    """
    FastAPI dependency for database sessions.
    
    Yields a database session and ensures it's properly closed
    after the request is completed.
    
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ DATABASE INITIALIZATION ============

def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    Creates all tables defined in the SQLAlchemy models.
    Safe to call multiple times - will only create tables that don't exist.
    
    Usage:
        from database.database import init_db
        init_db()
    """
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized successfully at: {DATABASE_URL}")


def drop_all_tables() -> None:
    """
    Drop all tables from the database.
    
    WARNING: This will delete all data! Use only for testing or development.
    
    Usage:
        from database.database import drop_all_tables
        drop_all_tables()
    """
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully")


def reset_db() -> None:
    """
    Reset the database by dropping and recreating all tables.
    
    WARNING: This will delete all data! Use only for development or testing.
    Equivalent to calling drop_all_tables() followed by init_db().
    
    Usage:
        from database.database import reset_db
        reset_db()
    """
    print("Resetting database...")
    drop_all_tables()
    init_db()
    print("Database reset complete")


# ============ HELPER FUNCTIONS ============

def get_database_url() -> str:
    """
    Get the current database URL being used.
    
    Returns:
        str: The database connection URL
    """
    return DATABASE_URL


def is_sqlite() -> bool:
    """
    Check if the current database is SQLite.
    
    Returns:
        bool: True if using SQLite, False otherwise
    """
    return DATABASE_URL.startswith("sqlite")


def is_postgresql() -> bool:
    """
    Check if the current database is PostgreSQL.
    
    Returns:
        bool: True if using PostgreSQL, False otherwise
    """
    return DATABASE_URL.startswith("postgresql")


# ============ MODULE INITIALIZATION ============

# Print database configuration on import (optional, can be removed for production)
if __name__ != "__main__":
    db_type = "SQLite" if is_sqlite() else "PostgreSQL" if is_postgresql() else "Other"
    print(f"Database configured: {db_type}")
