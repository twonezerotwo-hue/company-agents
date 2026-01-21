import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging
from dotenv import load_dotenv
from datetime import datetime

from models import Base, User, Agent, Task, TaskExecution, AgentLog
from schemas import (
    UserCreate, UserResponse, AgentCreate, AgentResponse,
    TaskCreate, TaskUpdate, TaskResponse, TaskExecutionResponse
)

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/company_agents"
)

database = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database)

# Create tables
Base.metadata.create_all(bind=database)

# FastAPI App
app = FastAPI(
    title="Company Agents API",
    description="AI Agent System for Automated Tasks",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Company Agents API is running!", "status": "active"}

@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# ============================================
# USER ENDPOINTS
# ============================================

@app.post("/users", response_model=UserResponse, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password (simple example - use bcrypt in production)
    password_hash = hash(user.password)
    
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=str(password_hash)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserResponse], tags=["Users"])
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all users"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# ============================================
# AGENT ENDPOINTS
# ============================================

@app.post("/agents", response_model=AgentResponse, tags=["Agents"])
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent"""
    db_agent = Agent(
        name=agent.name,
        role=agent.role,
        description=agent.description,
        status=agent.status
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    logger.info(f"Created agent: {db_agent.name}")
    return db_agent

@app.get("/agents", response_model=list[AgentResponse], tags=["Agents"])
async def list_agents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all agents"""
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

@app.get("/agents/{agent_id}", response_model=AgentResponse, tags=["Agents"])
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.put("/agents/{agent_id}", response_model=AgentResponse, tags=["Agents"])
async def update_agent(agent_id: int, agent_update: AgentCreate, db: Session = Depends(get_db)):
    """Update agent"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db_agent.name = agent_update.name
    db_agent.role = agent_update.role
    db_agent.description = agent_update.description
    db_agent.status = agent_update.status
    db_agent.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.delete("/agents/{agent_id}", tags=["Agents"])
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete agent"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    return {"message": "Agent deleted successfully"}

# ============================================
# TASK ENDPOINTS
# ============================================

@app.post("/tasks", response_model=TaskResponse, tags=["Tasks"])
async def create_task(task: TaskCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new task"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_task = Task(
        user_id=user_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        agent_id=task.agent_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Created task: {db_task.title}")
    return db_task

@app.get("/tasks", response_model=list[TaskResponse], tags=["Tasks"])
async def list_tasks(user_id: int = None, status: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List tasks with optional filters"""
    query = db.query(Task)
    
    if user_id:
        query = query.filter(Task.user_id == user_id)
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

# ============================================
# TASK EXECUTION ENDPOINTS
# ============================================

@app.post("/tasks/{task_id}/execute", response_model=TaskExecutionResponse, tags=["Task Execution"])
async def execute_task(task_id: int, agent_id: int, db: Session = Depends(get_db)):
    """Execute a task with an agent"""
    # Verify task and agent exist
    task = db.query(Task).filter(Task.id == task_id).first()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Create execution record
    execution = TaskExecution(
        task_id=task_id,
        agent_id=agent_id,
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    logger.info(f"Started execution of task {task_id} with agent {agent_id}")
    return execution

@app.get("/executions/{execution_id}", response_model=TaskExecutionResponse, tags=["Task Execution"])
async def get_execution(execution_id: int, db: Session = Depends(get_db)):
    """Get execution by ID"""
    execution = db.query(TaskExecution).filter(TaskExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution

@app.get("/executions", response_model=list[TaskExecutionResponse], tags=["Task Execution"])
async def list_executions(task_id: int = None, agent_id: int = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List executions with optional filters"""
    query = db.query(TaskExecution)
    
    if task_id:
        query = query.filter(TaskExecution.task_id == task_id)
    if agent_id:
        query = query.filter(TaskExecution.agent_id == agent_id)
    
    executions = query.offset(skip).limit(limit).all()
    return executions

@app.put("/executions/{execution_id}", tags=["Task Execution"])
async def update_execution(execution_id: int, status: str, result: str = None, error_message: str = None, db: Session = Depends(get_db)):
    """Update execution status and result"""
    execution = db.query(TaskExecution).filter(TaskExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    execution.status = status
    if result:
        execution.result = result
    if error_message:
        execution.error_message = error_message
    
    if status == "completed" or status == "failed":
        execution.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(execution)
    return execution

# ============================================
# AGENT LOGS ENDPOINTS
# ============================================

@app.post("/logs", tags=["Logs"])
async def create_log(agent_id: int, log_level: str, message: str, execution_id: int = None, db: Session = Depends(get_db)):
    """Create an agent log"""
    # Verify agent exists
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    log = AgentLog(
        agent_id=agent_id,
        execution_id=execution_id,
        log_level=log_level,
        message=message
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@app.get("/logs", tags=["Logs"])
async def list_logs(agent_id: int = None, execution_id: int = None, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List agent logs"""
    query = db.query(AgentLog)
    
    if agent_id:
        query = query.filter(AgentLog.agent_id == agent_id)
    if execution_id:
        query = query.filter(AgentLog.execution_id == execution_id)
    
    logs = query.order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)