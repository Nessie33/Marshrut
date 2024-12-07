from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import *
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks


@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_task(user_id: int, task: CreateTask, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    new_task = Task(**task.dict(), user_id=user_id)
    db.add(new_task)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{task_id}', status_code=status.HTTP_201_CREATED)
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    dop_task = db.execute(select(User).where(Task.id == task_id)).scalar_one_or_none()
    if dop_task is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(Task).where(Task.id == task_id).values(**task.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete('/delete/{task_id}', status_code=status.HTTP_201_CREATED)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    dop_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if dop_task is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK}