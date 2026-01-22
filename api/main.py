import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal, Base, init_db
from models import Holding, Company, Department, Agent, User, Task
from schemas import (HoldingCreate, HoldingResponse, HoldingWithCompanies, CompanyCreate, CompanyResponse, CompanyWithDepartments, DepartmentCreate, DepartmentResponse, DepartmentWithAgents, AgentCreate, AgentResponse, AgentWithTasks, TaskCreate, TaskResponse, TaskUpdate, UserCreate, UserResponse)

app = FastAPI()

# Create all tables on startup
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# ===== HOLDINGS CRUD =====
@app.post("/holdings/", response_model=HoldingResponse)
def create_holding(holding: HoldingCreate, db: Session = Depends(get_db)):
    db_holding = Holding(**holding.dict())
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

@app.get("/holdings/", response_model=List[HoldingWithCompanies])
def read_holdings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    holdings = db.query(Holding).offset(skip).limit(limit).all()
    return holdings

@app. put("/holdings/{holding_id}", response_model=HoldingResponse)
def update_holding(holding_id: int, holding: HoldingCreate, db: Session = Depends(get_db)):
    db_holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not db_holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    for key, value in holding.dict().items():
        setattr(db_holding, key, value)
    db.commit()
    return db_holding

@app.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    db_holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not db_holding: 
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(db_holding)
    db.commit()
    return {"detail": "Holding deleted"}

# ===== COMPANIES CRUD =====
@app.post("/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db:  Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/companies/", response_model=List[CompanyWithDepartments])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db. query(Company).offset(skip).limit(limit).all()
    return companies

@app.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(company_id:  int, company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    return db_company

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"detail": "Company deleted"}

# ===== DEPARTMENTS CRUD =====
@app.post("/departments/", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@app.get("/departments/", response_model=List[DepartmentWithAgents])
def read_departments(skip: int = 0, limit:  int = 100, db: Session = Depends(get_db)):
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments

@app.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in department.dict().items():
        setattr(db_department, key, value)
    db.commit()
    return db_department

@app.delete("/departments/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_department)
    db.commit()
    return {"detail": "Department deleted"}

# ===== AGENTS CRUD =====
@app.post("/agents/", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.get("/agents/", response_model=List[AgentWithTasks])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

@app.put("/agents/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    for key, value in agent.dict().items():
        setattr(db_agent, key, value)
    db.commit()
    return db_agent

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db:  Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(db_agent)
    db.commit()
    return {"detail": "Agent deleted"}

# ===== TASKS CRUD =====
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task:  TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task. dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id:  int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}

# ===== USERS CRUD =====
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app. get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user

@app. delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8080)