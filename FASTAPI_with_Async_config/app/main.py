from re import L

from fastapi import FastAPI
from pydantic import BaseModel
from app.user import services as   user_serives

app = FastAPI(title="welcome to the world of fastapi with sqlalchemy or alembic")

class UserData(BaseModel):
    id:int|None = None
    name:str | None = None
    email:str

@app.post("/user")

async def create_user(user:UserData):
    user = await user_serives.create_user(user.name,user.email)
    return {"status":"user created successfully"}


@app.get("/")
async def get_users():
    user = await user_serives.get_user_data()
    return user

@app.get("/user/{user_id}")
async def get_user_by_id(user_id:int):
    user = await user_serives.get_user_by_id(user_id)
    return user

@app.put("/update")
async def update_user(newdata:UserData):
    user = await user_serives.update_user_name_email(newdata.id,newdata.name,newdata.email)
    return user

@app.delete("/delete")
async def delelte_user(user_id):
    user = await user_serives.delete_user(user_id)
    return {"status ":"user successful deleted!"}