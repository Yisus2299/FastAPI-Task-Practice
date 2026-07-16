from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from model import User, Task

router = APIRouter(
    prefix= "/admin",
    tags=["Admin"]
)

FIXED_USER_ID = 1

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    
    # Count total tasks
    total_tasks = db.query(Task).count()
    
    # Count total users
    total_users = db.query(User).count()
    
    # Count completed tasks (completed = True)
    completed_tasks = db.query(Task).filter(Task.completed == True).count()
    
    # Count pending tasks (completed = False)
    pending_tasks = db.query(Task).filter(Task.completed == False).count()
    
    # Calculating the average of tasks by user: Using func.avg()
    avg_tasks_per_user = db.query(func.avg(Task.user_id)).scalar() or 0
    
    return {
        "total_tasks": total_tasks,
        "total_users": total_users,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "avg_tasks_per_user": round(avg_tasks_per_user, 2)
    }