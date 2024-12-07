from fastapi import FastAPI
from app.routers.task import router as task
from app.routers.user import router as user


app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task)
app.include_router(user)