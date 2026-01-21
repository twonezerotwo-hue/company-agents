from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class Agent(BaseModel):
    __tablename__ = 'agents'
    # Define agent fields here

class User(BaseModel):
    __tablename__ = 'users'
    # Define user fields here

class Task(BaseModel):
    __tablename__ = 'tasks'
    # Define task fields here