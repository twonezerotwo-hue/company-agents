"""
API Database Configuration - Import from database package

This file now imports all database utilities from the database package
for backward compatibility.
"""

from database import (
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db,
    drop_all_tables,
    reset_db,
)

__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "init_db",
    "drop_all_tables",
    "reset_db",
]