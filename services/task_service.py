from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status

from model import Task
from schemas import TaskCreate, TaskUpdateStatus

#1- GET method all tasks
def get_all_tasks_service(
    db: Session,
    user_id: int,
    completed: Optional[bool] = None,
    description: Optional[str] = None,
    title: Optional[str] = None,
    order: Optional[str] = "asc",
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    limit: Optional[int] = None
    ) -> List[Task]:
    
    tasks = db.query(Task).filter(Task.user_id == user_id)
    if completed is not None:
        tasks = tasks.filter(Task.completed == completed)
    if title:
        tasks = tasks.filter(Task.title.ilike(f"%{title}%"))
    
    if description:
        tasks = tasks.filter(Task.title.ilike(f"%{description}%"))
    
    if id_min is not None:
        tasks = tasks.filter(Task.id >= id_min)
        
    if id_max is not None:
        tasks = tasks.filter(Task.id <= id_max)
    

    # Order priority by desc
    tasks = tasks.order_by(Task.priority.desc())
    
    if order == "desc":
        tasks = tasks.order_by(Task.id.desc())
    elif order == "asc":
        tasks = tasks.order_by(Task.id.asc())
    
    if limit is not None:
        tasks = tasks.limit(limit)

    
    return tasks.all()

#2- GET method, get a single Task
def get_task_service(
    task_id: int, 
    db: Session
    ) -> Task:
    single_task = db.query(Task).filter(Task.id==task_id).first()
    if not single_task:
        raise HTTPException(detail=f"the task with the id {task_id} can't be found", status_code=404)
    return single_task

#3- POST method: create a task

def task_create_service(
    task_create: TaskCreate, 
    db:Session,
    user_id: int
    ) -> Task:
    
    # added Active Tasks:
    active_tasks_count = db.query(Task).filter(
    Task.user_id == user_id,
    Task.completed == False
    ).count()
    
    # Asign priority based on the number of active tasks
    if active_tasks_count > 5:
        priority = 3
    elif active_tasks_count > 3:
        priority = 2
    else:
        priority = 1
 
    # create Task with the priority
    new_task = Task(
        title = task_create.title,
        description = task_create.description,
        user_id = user_id,
        priority = priority
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#4- PUT method: Update Complete status:
def updated_task_service(
    completed: bool, 
    task_id: int ,
    db: Session,
    user_id: int
) -> Task:
    exist = db.query(Task).filter(Task.id==task_id).first()
    if not exist:
        raise HTTPException(detail=f"the task with the id: {task_id} is not found", status_code=404)
    
    #added verification
    if exist.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this task"        
        )
    
    
    exist.completed= completed
    
    db.commit()
    db.refresh(exist)
    return exist

# 5- DELETE: Delete a Task:
def delete_task_service(
    task_id: int ,
    db:Session,
    user_id: int
    ) -> Task:
    task_delete = db.query(Task).filter(Task.id == task_id).first()
    if not task_delete:
        raise HTTPException(detail="The task can't be found", status_code=404)
    if task_delete.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this task"
        )
    
    db.delete(task_delete)
    db.commit()
    return None

