from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.get('/{user_id}/tasks')
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return tasks


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{user_id}', status_code=status.HTTP_201_CREATED)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    dop_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if dop_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(User).where(User.id == user_id).values(**user.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete/{user_id}', status_code=status.HTTP_201_CREATED)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    dop_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if dop_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK}