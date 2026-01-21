import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Agent(BaseModel):
    id: int
    name: str
    task_ids: List[int]

class User(BaseModel):
    id: int
    username: str
    agent_ids: List[int]

class Task(BaseModel):
    id: int
    title: str
    description: str

# Sample FastAPI endpoints
@app.get("/agents/", response_model=List[Agent])
async def get_agents():
    return []  # Should return a list of agents

@app.post("/agents/", response_model=Agent)
async def create_agent(agent: Agent):
    return agent  # Should create an agent

@app.get("/users/", response_model=List[User])
async def get_users():
    return []  # Should return a list of users

@app.post("/users/", response_model=User)
async def create_user(user: User):
    return user  # Should create a user

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return []  # Should return a list of tasks

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    return task  # Should create a task

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)