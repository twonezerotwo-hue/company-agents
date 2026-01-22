"""
Database Package Initialization

This package contains all database-related components:
- models.py: SQLAlchemy ORM models and enums
- database.py: Database configuration and session management
"""

from database.models import (
    Base,
    StatusEnum,
    PriorityEnum,
    TaskStatusEnum,
    Holding,
    Company,
    Department,
    User,
    Agent,
    Task,
    TaskExecution,
    AgentLog,
)

from database.database import (
    engine,
    SessionLocal,
    get_db,
    init_db,
    drop_all_tables,
    reset_db,
    get_database_url,
    is_sqlite,
    is_postgresql,
)

__all__ = [
    # Models
    "Base",
    "StatusEnum",
    "PriorityEnum",
    "TaskStatusEnum",
    "Holding",
    "Company",
    "Department",
    "User",
    "Agent",
    "Task",
    "TaskExecution",
    "AgentLog",
    # Database functions
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "drop_all_tables",
    "reset_db",
    "get_database_url",
    "is_sqlite",
    "is_postgresql",
]
