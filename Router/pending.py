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
