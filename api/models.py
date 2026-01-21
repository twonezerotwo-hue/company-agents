from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    user = relationship('User', back_populates='agents')
    tasks = relationship('Task', back_populates='agent')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    agent_id = Column(Integer, ForeignKey('agents.id'))
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
