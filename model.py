from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, index=True, primary_key=True)
    email = Column(String, index=True, unique=True)
    
    tasks = relationship("Task", back_populates="owner")
    

class Task(Base):
    __tablename__="task"
    
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")