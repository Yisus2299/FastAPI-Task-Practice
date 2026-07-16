from pydantic import BaseModel, field_validator
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True

# Tasks Schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    
    # personalized valitadors apply only for Create schemas, which are
    # the ones the user sees, reponse is what we see (backend)

    # personalized validators for title: 1
    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise ValueError("Title must have at least 3 characters")
        return value
    
    # validators for description: 2
    @field_validator('description')
    @classmethod
    def send_description(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and len(value.strip()) < 5:
            raise ValueError("Description must have at least 5 characters")
        return value
    

class TaskUpdateStatus(BaseModel):
    completed: bool

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int
    completed: bool
    owner: Optional[UserResponse] = None
    priority = int
    
    class Config:
        from_attributes = True