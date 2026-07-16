from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from model import Task
from schemas import TaskCreate, TaskResponse
from services.task_service import create_task_service

router = APIRouter(
    prefix="/pending-tasks" ,
    tags= ["Pending Tasks"]
)


pending_tasks = {}

FIXED_USER_ID = 1

# GET ENDPOINT:

@router.get("")
def get_pending_task():
    
    user_pending = pending_tasks.get(FIXED_USER_ID, [])
    
    return{
        "user_id": FIXED_USER_ID,
        "pending_tasks": user_pending,
        "total": len(user_pending)
    }

# POST ENDPOINT:

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_pending_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    user_pending = pending_tasks.get(FIXED_USER_ID, [])
    
    for existing_task in user_pending:
        if existing_task["title"].lower() == task.title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "A pending task with this title already exists"
            )
    
    new_pending_task = {
        "title":task.title,
        "description":task.description
    }
    user_pending.append(new_pending_task)
    
    pending_tasks[FIXED_USER_ID] = user_pending
    
    return{
        "message": "Task added to pending list",
        "pending_tasks": user_pending
    }
    
# DELETE ENDPOINT:

@router.delete("/{task_index}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pending_task(task_index:int):
    user_pending = pending_tasks.get(FIXED_USER_ID, [])
    
    if task_index < 0 or task_index >= len(user_pending):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task index out of range"
        )
        
    deleted_task = user_pending.pop(task_index)
    
    pending_tasks[FIXED_USER_ID] = user_pending
    
    return None

# OPTIONAL ENDPOINT (COMMIT):
@router.post("/commit", status_code=status.HTTP_201_CREATED)
def commit_pending_tasks(db: Session = Depends(get_db)):
  
    user_pending = pending_tasks.get(FIXED_USER_ID, [])
    
    if not user_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending tasks to commit"
        )
    

    created_tasks = []
    for pending_task in user_pending:

        task_create = TaskCreate(
            title=pending_task["title"],
            description=pending_task.get("description")
        )

        new_task = create_task_service(
            db=db,
            task_create=task_create,
            user_id=FIXED_USER_ID
        )
        created_tasks.append(new_task)
    
  
    pending_tasks[FIXED_USER_ID] = []
    
  
    return {
        "message": f"{len(created_tasks)} tasks committed successfully",
        "created_tasks": created_tasks
    }
    