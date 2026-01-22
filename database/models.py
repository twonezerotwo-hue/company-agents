"""
SQLAlchemy ORM Models for Company Agents System

Defines all database models with proper relationships, cascade deletes,
timestamps, and enum types for status tracking.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()


# ============ ENUMS ============
class StatusEnum(str, enum.Enum):
    """Status for agents and general entities"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class PriorityEnum(str, enum.Enum):
    """Priority levels for tasks"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatusEnum(str, enum.Enum):
    """Status for task lifecycle"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============ MODELS ============
class Holding(Base):
    """
    Top-level organizational unit that contains companies.
    Represents a holding company or parent organization.
    """
    __tablename__ = 'holdings'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    companies = relationship(
        'Company',
        back_populates='holding',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    def __repr__(self):
        return f"<Holding(id={self.id}, name='{self.name}')>"


class Company(Base):
    """
    Company entity that belongs to a Holding and contains Departments.
    Represents an individual company within a holding.
    """
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(500))
    holding_id = Column(Integer, ForeignKey('holdings.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    holding = relationship('Holding', back_populates='companies')
    departments = relationship(
        'Department',
        back_populates='company',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_company_holding', 'holding_id'),
    )
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', holding_id={self.holding_id})>"


class Department(Base):
    """
    Department within a Company that contains Agents.
    Represents a functional unit or team.
    """
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(500))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship('Company', back_populates='departments')
    agents = relationship(
        'Agent',
        back_populates='department',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_department_company', 'company_id'),
    )
    
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', company_id={self.company_id})>"


class User(Base):
    """
    System user account that can be associated with Agents.
    Represents a person who uses the system.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    agents = relationship(
        'Agent',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Agent(Base):
    """
    Employee or agent within a Department, optionally linked to a User.
    Represents an autonomous agent or employee who can be assigned tasks.
    """
    __tablename__ = 'agents'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    role = Column(String(255), nullable=False)
    description = Column(String(500))
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    department_id = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='agents')
    department = relationship('Department', back_populates='agents')
    tasks = relationship(
        'Task',
        back_populates='agent',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_agent_department', 'department_id'),
        Index('idx_agent_user', 'user_id'),
        Index('idx_agent_status', 'status'),
    )
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', role='{self.role}', status='{self.status}')>"


class Task(Base):
    """
    Task that can be assigned to an Agent.
    Represents work items with priority and status tracking.
    """
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(1000))
    priority = Column(SQLEnum(PriorityEnum), default=PriorityEnum.MEDIUM, nullable=False, index=True)
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.PENDING, nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey('agents.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    agent = relationship('Agent', back_populates='tasks')
    executions = relationship(
        'TaskExecution',
        back_populates='task',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_task_agent', 'agent_id'),
        Index('idx_task_status', 'status'),
        Index('idx_task_priority', 'priority'),
        Index('idx_task_status_priority', 'status', 'priority'),
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"


class TaskExecution(Base):
    """
    Execution record for a Task.
    Tracks when tasks are executed and their results.
    """
    __tablename__ = 'task_executions'
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    task = relationship('Task', back_populates='executions')
    
    # Indexes
    __table_args__ = (
        Index('idx_execution_task', 'task_id'),
        Index('idx_execution_executed_at', 'executed_at'),
    )
    
    def __repr__(self):
        return f"<TaskExecution(id={self.id}, task_id={self.task_id}, executed_at='{self.executed_at}')>"


class AgentLog(Base):
    """
    Log entries for Agent activities.
    Tracks agent actions and events for auditing and debugging.
    """
    __tablename__ = 'agent_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey('agents.id', ondelete='CASCADE'), nullable=False)
    log_message = Column(String(1000), nullable=False)
    log_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    agent = relationship('Agent')
    
    # Indexes
    __table_args__ = (
        Index('idx_log_agent', 'agent_id'),
        Index('idx_log_time', 'log_time'),
    )
    
    def __repr__(self):
        return f"<AgentLog(id={self.id}, agent_id={self.agent_id}, log_time='{self.log_time}')>"
