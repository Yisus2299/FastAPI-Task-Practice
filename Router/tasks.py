from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from model import Task
from schemas import TaskCreate, TaskUpdateStatus, TaskResponse

from services.task_service import (
    get_all_tasks_service,
    get_task_service,
    task_create_service,
    updated_task_service,
    delete_task_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

FIXED_USER_ID = 1


# Tasks ENDPOINTS with filters incluying user:
@router.get("", response_model=List[TaskResponse])
def get_all_tasks_service(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    description: Optional[str] = None,
    title: Optional[str] = None,
    order: Optional[str] = "asc",
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    limit: Optional[int] = None
    ):

        return get_all_tasks_service(
            db=db,
            user_id = FIXED_USER_ID,
            completed=completed,
            title=title,
            description=description,
            id_min=id_min,
            id_max=id_max,
            order=order,
            limit=limit           
        )

@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_service(db=db, task_id=task_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def task_create(
    task_create: TaskCreate, 
    db:Session = Depends(get_db)
    ):
        return task_create_service(db=db, task_create=task_create, user_id=FIXED_USER_ID)

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def updated_task(
    status_task: TaskUpdateStatus, 
    task_id: int ,
    db: Session = Depends(get_db),
):
    return updated_task_service(
        db=db,
        task_id=task_id,
        completed=status_task.completed,
        user_id=FIXED_USER_ID
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int ,
    db:Session = Depends(get_db)):
    delete_task_service(db=db, task_id=task_id, user_id=FIXED_USER_ID)
    return None