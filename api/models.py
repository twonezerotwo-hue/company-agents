from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Holding(Base):
    __tablename__ = 'holdings'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    companies = relationship('Company', back_populates='holding')

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    holding_id = Column(Integer, ForeignKey('holdings.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    holding = relationship('Holding', back_populates='companies')
    departments = relationship('Department', back_populates='company')

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company = relationship('Company', back_populates='departments')
    agents = relationship('Agent', back_populates='department')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    agents = relationship('Agent', back_populates='user')

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    role = Column(String)
    description = Column(String)
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', back_populates='agents')
    department = relationship('Department', back_populates='agents')
    tasks = relationship('Task', back_populates='agent')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    priority = Column(String, default='medium')
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    agent = relationship('Agent', back_populates='tasks')
    executions = relationship('TaskExecution', back_populates='task')

class TaskExecution(Base):
    __tablename__ = 'task_executions'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    executed_at = Column(DateTime)
    result = Column(JSON)
    task = relationship('Task', back_populates='executions')

class AgentLog(Base):
    __tablename__ = 'agent_logs'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    log_message = Column(String)
    log_time = Column(DateTime)
    agent = relationship('Agent')