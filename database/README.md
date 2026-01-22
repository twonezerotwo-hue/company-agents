# Database Package Documentation

This document describes the SQLAlchemy ORM models and database configuration for the company-agents project.

## Overview

The database package provides:
- Complete ORM models for the company hierarchy
- Database connection and session management
- Support for SQLite (default) and PostgreSQL
- Proper cascade delete relationships
- Enum types for status tracking
- Index optimization for common queries

## Quick Start

### 1. Initialize Database

```python
from database import init_db

# Create all tables
init_db()
```

### 2. Using with FastAPI

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Holding

app = FastAPI()

@app.get("/holdings/")
def read_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).all()
```

### 3. Direct Database Access

```python
from database import SessionLocal, Holding, Company, StatusEnum

# Create a session
db = SessionLocal()

try:
    # Create a holding
    holding = Holding(name="My Holding", description="Test holding")
    db.add(holding)
    db.commit()
    db.refresh(holding)
    
    # Create a company
    company = Company(
        name="My Company",
        description="Test company",
        holding_id=holding.id
    )
    db.add(company)
    db.commit()
finally:
    db.close()
```

## Database Models

### Holding
Top-level organizational unit that contains companies.

**Fields:**
- `id` (int): Primary key
- `name` (str): Unique name
- `description` (str): Optional description
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `companies` (relationship): List of associated companies

### Company
Company entity that belongs to a Holding and contains Departments.

**Fields:**
- `id` (int): Primary key
- `name` (str): Company name
- `description` (str): Optional description
- `holding_id` (int): Foreign key to Holding
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `holding` (relationship): Parent holding
- `departments` (relationship): List of departments

### Department
Department within a Company that contains Agents.

**Fields:**
- `id` (int): Primary key
- `name` (str): Department name
- `description` (str): Optional description
- `company_id` (int): Foreign key to Company
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `company` (relationship): Parent company
- `agents` (relationship): List of agents

### User
System user account that can be associated with Agents.

**Fields:**
- `id` (int): Primary key
- `username` (str): Unique username
- `email` (str): Unique email address
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `agents` (relationship): List of associated agents

### Agent
Employee or agent within a Department, optionally linked to a User.

**Fields:**
- `id` (int): Primary key
- `name` (str): Agent name
- `role` (str): Agent role/title
- `description` (str): Optional description
- `status` (StatusEnum): Agent status (active, inactive, suspended)
- `user_id` (int): Optional foreign key to User
- `department_id` (int): Foreign key to Department
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `user` (relationship): Associated user
- `department` (relationship): Parent department
- `tasks` (relationship): List of assigned tasks

### Task
Task that can be assigned to an Agent.

**Fields:**
- `id` (int): Primary key
- `title` (str): Task title
- `description` (str): Task description
- `priority` (PriorityEnum): Priority level (low, medium, high, urgent)
- `status` (TaskStatusEnum): Task status (pending, in_progress, completed, failed, cancelled)
- `agent_id` (int): Optional foreign key to Agent
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `agent` (relationship): Assigned agent
- `executions` (relationship): List of task executions

### TaskExecution
Execution record for a Task.

**Fields:**
- `id` (int): Primary key
- `task_id` (int): Foreign key to Task
- `executed_at` (datetime): Execution timestamp
- `result` (JSON): Execution result data
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `task` (relationship): Parent task

### AgentLog
Log entries for Agent activities.

**Fields:**
- `id` (int): Primary key
- `agent_id` (int): Foreign key to Agent
- `log_message` (str): Log message
- `log_time` (datetime): Log timestamp
- `created_at` (datetime): Creation timestamp
- `agent` (relationship): Associated agent

## Enums

### StatusEnum
Status values for agents and general entities.

**Values:**
- `ACTIVE`: "active"
- `INACTIVE`: "inactive"
- `SUSPENDED`: "suspended"

### PriorityEnum
Priority levels for tasks.

**Values:**
- `LOW`: "low"
- `MEDIUM`: "medium"
- `HIGH`: "high"
- `URGENT`: "urgent"

### TaskStatusEnum
Status values for task lifecycle.

**Values:**
- `PENDING`: "pending"
- `IN_PROGRESS`: "in_progress"
- `COMPLETED`: "completed"
- `FAILED`: "failed"
- `CANCELLED`: "cancelled"

## Configuration

### Environment Variables

**DATABASE_URL**: Database connection URL
- Default: `sqlite:///./company_agents.db`
- PostgreSQL example: `postgresql://user:password@localhost:5432/dbname`

### Database Functions

#### `init_db()`
Initialize the database by creating all tables.

```python
from database import init_db
init_db()
```

#### `drop_all_tables()`
⚠️ **WARNING**: Deletes all data!

Drop all tables from the database.

```python
from database import drop_all_tables
drop_all_tables()
```

#### `reset_db()`
⚠️ **WARNING**: Deletes all data!

Reset the database by dropping and recreating all tables.

```python
from database import reset_db
reset_db()
```

#### `get_db()`
FastAPI dependency for database sessions.

```python
from database import get_db
from fastapi import Depends

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

#### `get_database_url()`
Get the current database URL being used.

```python
from database import get_database_url
print(get_database_url())
```

#### `is_sqlite()`
Check if the current database is SQLite.

```python
from database import is_sqlite
if is_sqlite():
    print("Using SQLite")
```

#### `is_postgresql()`
Check if the current database is PostgreSQL.

```python
from database import is_postgresql
if is_postgresql():
    print("Using PostgreSQL")
```

## Features

### Cascade Delete
All relationships use cascade delete, so deleting a parent will automatically delete its children:

- Deleting a Holding deletes all its Companies
- Deleting a Company deletes all its Departments
- Deleting a Department deletes all its Agents
- Deleting an Agent deletes all its Tasks
- Deleting a Task deletes all its TaskExecutions

### Indexes
The following indexes are created for query optimization:

**Holding:**
- `name` (unique index)

**Company:**
- `name` (index)
- `holding_id` (index)

**Department:**
- `name` (index)
- `company_id` (index)

**User:**
- `username` (unique index)
- `email` (unique index)

**Agent:**
- `name` (index)
- `status` (index)
- `department_id` (index)
- `user_id` (index)

**Task:**
- `title` (index)
- `priority` (index)
- `status` (index)
- `agent_id` (index)
- `status, priority` (composite index)

**TaskExecution:**
- `task_id` (index)
- `executed_at` (index)

**AgentLog:**
- `agent_id` (index)
- `log_time` (index)

### Timestamps
All models include `created_at` and `updated_at` timestamps that are automatically managed:

- `created_at`: Set when the record is created
- `updated_at`: Set when the record is created and updated on every modification

## Examples

### Example 1: Complete Hierarchy

```python
from database import (
    SessionLocal, Holding, Company, Department,
    User, Agent, Task, StatusEnum, PriorityEnum, TaskStatusEnum
)

db = SessionLocal()

# Create holding
holding = Holding(name="Tech Corp", description="Technology holding company")
db.add(holding)
db.commit()
db.refresh(holding)

# Create company
company = Company(
    name="Software Inc",
    description="Software development company",
    holding_id=holding.id
)
db.add(company)
db.commit()
db.refresh(company)

# Create department
department = Department(
    name="Engineering",
    description="Software engineering department",
    company_id=company.id
)
db.add(department)
db.commit()
db.refresh(department)

# Create user
user = User(username="john.doe", email="john@example.com")
db.add(user)
db.commit()
db.refresh(user)

# Create agent
agent = Agent(
    name="John Doe",
    role="Senior Developer",
    status=StatusEnum.ACTIVE,
    user_id=user.id,
    department_id=department.id
)
db.add(agent)
db.commit()
db.refresh(agent)

# Create task
task = Task(
    title="Implement feature X",
    description="Add new feature to the system",
    priority=PriorityEnum.HIGH,
    status=TaskStatusEnum.PENDING,
    agent_id=agent.id
)
db.add(task)
db.commit()

db.close()
```

### Example 2: Querying with Relationships

```python
from database import SessionLocal, Holding

db = SessionLocal()

# Get holding with all related data
holding = db.query(Holding).first()
print(f"Holding: {holding.name}")

for company in holding.companies:
    print(f"  Company: {company.name}")
    
    for department in company.departments:
        print(f"    Department: {department.name}")
        
        for agent in department.agents:
            print(f"      Agent: {agent.name} ({agent.status.value})")
            
            for task in agent.tasks:
                print(f"        Task: {task.title} [{task.status.value}]")

db.close()
```

### Example 3: Using Enums

```python
from database import SessionLocal, Agent, Task, StatusEnum, TaskStatusEnum

db = SessionLocal()

# Query by enum value
active_agents = db.query(Agent).filter(Agent.status == StatusEnum.ACTIVE).all()
print(f"Active agents: {len(active_agents)}")

# Query pending tasks
pending_tasks = db.query(Task).filter(Task.status == TaskStatusEnum.PENDING).all()
print(f"Pending tasks: {len(pending_tasks)}")

# Update status
task = db.query(Task).first()
task.status = TaskStatusEnum.IN_PROGRESS
db.commit()

db.close()
```

## Migration from Old Code

If you have existing code using `api/database.py` or `api/models.py`, no changes are required. The API files now import from the database package, maintaining backward compatibility.

```python
# Old code - still works
from database import Base, engine, SessionLocal
from models import Holding, Company, Agent

# New code - preferred
from database import Base, engine, SessionLocal, Holding, Company, Agent
```

## Testing

For development and testing, you can use the utility functions:

```python
from database import reset_db

# Reset database for testing
reset_db()

# Run your tests...
```

Or use environment variables:

```bash
# Use in-memory SQLite for tests
export DATABASE_URL="sqlite:///:memory:"
python -m pytest

# Use test PostgreSQL database
export DATABASE_URL="postgresql://user:pass@localhost/test_db"
python -m pytest
```
