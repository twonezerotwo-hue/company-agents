from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class AgentCreate(BaseModel):
    name: str
    role: str
    description: str
    status: str = "active"

class AgentResponse(BaseModel):
    id: int
    name: str
    role: str
    description: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    agent_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    agent_id: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    priority: str
    status: str
    agent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class TaskExecutionResponse(BaseModel):
    id: int
    task_id: int
    agent_id: int
    status: str
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class AgentLogResponse(BaseModel):
    id: int
    agent_id: int
    execution_id: Optional[int] = None
    log_level: str
    message: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True