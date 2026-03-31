from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from app.db.config import create_tables,SessionDep
from app.task.model import Task
from sqlmodel import select

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan,title="welcome to the world of the fastapi!")


@app.post("/create_task")
def create_task(title:str,content:str,session:SessionDep):
    task = Task(title=title,content=content)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"task created successfully":task}


@app.get("/")
def get_task(session:SessionDep):
    task = session.exec(select(Task)).all()
    if not task:
        raise HTTPException(status_code=404,detail="you task not found!")
    return task


@app.get("/task/{task_id}")

def task_with_id(task_id:int,session:SessionDep):
    task = session.get(Task,task_id)
    if not task:
        raise HTTPException(status_code=404,detail="Task id not found!")
    return task


@app.put("/update_task")
def update_task(task_id:int,update_title:str,update_content:str,session:SessionDep):
    task = session.get(Task,task_id)
    if not task:
        raise HTTPException(status_code=404,detail="task id not found!")
    
    task.title = update_title
    task.content = update_content
    session.commit()
    session.refresh(task)
    return task

@app.delete("/delete_task")
def delete_task(task_id:int,session:SessionDep):
    task = session.get(Task,task_id)
    if not task:
        raise HTTPException(status_code=404,detail="task not found ! sorry")
    session.delete(task)
    session.commit()
    return {"task deleted successfully":task}