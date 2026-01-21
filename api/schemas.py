from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============ HOLDING SCHEMAS ============
class HoldingCreate(BaseModel):
    name: str
    description: Optional[str] = None

class HoldingResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class HoldingWithCompanies(HoldingResponse):
    companies: List['CompanyResponse'] = []

# ============ COMPANY SCHEMAS ============
class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    holding_id: int

class CompanyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    holding_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class CompanyWithDepartments(CompanyResponse):
    departments: List['DepartmentResponse'] = []

# ============ DEPARTMENT SCHEMAS ============
class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: int

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    company_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class DepartmentWithAgents(DepartmentResponse):
    agents: List['AgentResponse'] = []

# ============ USER SCHEMAS ============
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

# ============ AGENT SCHEMAS ============
class AgentCreate(BaseModel):
    name: str
    role: str
    description: Optional[str] = None
    status: str = "active"
    user_id: Optional[int] = None
    department_id: int

class AgentResponse(BaseModel):
    id: int
    name: str
    role: str
    description: Optional[str] = None
    status: str
    user_id: Optional[int] = None
    department_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class AgentWithTasks(AgentResponse):
    tasks: List['TaskResponse'] = []

# ============ TASK SCHEMAS ============
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
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
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    agent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ============ TASK EXECUTION SCHEMAS ============
class TaskExecutionResponse(BaseModel):
    id: int
    task_id: int
    executed_at: Optional[datetime] = None
    result: Optional[dict] = None
    class Config:
        from_attributes = True

# ============ AGENT LOG SCHEMAS ============
class AgentLogResponse(BaseModel):
    id: int
    agent_id: int
    log_message: str
    log_time: Optional[datetime] = None
    class Config:
        from_attributes = True

# Update forward references
HoldingWithCompanies.model_rebuild()
CompanyWithDepartments.model_rebuild()
DepartmentWithAgents.model_rebuild()
AgentWithTasks.model_rebuild()