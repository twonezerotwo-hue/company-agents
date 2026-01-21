# FastAPI Endpoints for Agents, Users, and Tasks Management

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Database Models (Mock)
class Agent:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

class User:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

class Task:
    def __init__(self, id: int, title: str, description: str, assigned_to: int):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to

# Pydantic Schemas
class AgentCreate(BaseModel):
    name: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int

# Mock databases
agents_db = []  # This would be a real database in production
users_db = []
tasks_db = []

# Endpoints

@app.post("/agents/", response_model=Agent)
async def create_agent(agent: AgentCreate):
    new_agent = Agent(id=len(agents_db)+1, **agent.dict())
    agents_db.append(new_agent)
    return new_agent

@app.get("/agents/", response_model=List[Agent])
async def get_agents():
    return agents_db

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    new_user = User(id=len(users_db)+1, **user.dict())
    users_db.append(new_user)
    return new_user

@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    new_task = Task(id=len(tasks_db)+1, **task.dict())
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks_db

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
