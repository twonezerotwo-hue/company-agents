import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
from models import Base, Holding, Company, Department, Agent, User, Task
from schemas import (HoldingCreate, HoldingResponse, HoldingWithCompanies, CompanyCreate, CompanyResponse, CompanyWithDepartments, DepartmentCreate, DepartmentResponse, DepartmentWithAgents, AgentCreate, AgentResponse, AgentWithTasks, TaskCreate, TaskResponse, TaskUpdate, UserCreate, UserResponse)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Holdings
@app.post("/holdings/", response_model=HoldingResponse)
def create_holding(holding: HoldingCreate, db: Session = Depends(get_db)):
    db_holding = Holding(**holding.dict())
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

# Read Holdings
@app.get("/holdings/", response_model=List[HoldingWithCompanies])
def read_holdings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    holdings = db.query(Holding).offset(skip).limit(limit).all()
    return holdings

# Update Holdings
@app.put("/holdings/{holding_id}", response_model=HoldingResponse)
def update_holding(holding_id: int, holding: HoldingCreate, db: Session = Depends(get_db)):
    db_holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not db_holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    for key, value in holding.dict().items():
        setattr(db_holding, key, value)
    db.commit()
    return db_holding

# Delete Holdings
@app.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    db_holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not db_holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(db_holding)
    db.commit()
    return {"detail": "Holding deleted"}

# Add CRUD for Companies, Departments, Agents, Tasks, and Users ... 
# Similar structure as Holdings but with their respective schemas and models
