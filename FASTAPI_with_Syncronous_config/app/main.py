from fastapi import FastAPI
from app.user import services as user_service
app = FastAPI(title="Fastapi with sqlalchemy with alembic migration master series")
from pydantic import BaseModel

class UserData(BaseModel):
    name:str
    email:str
    phone_no:int

class Update(BaseModel):
    user_id:int
    name:str

@app.post("/user")
def create_user(user:UserData):
    user = user_service.create_user(user.name,user.email,user.phone_no)
    return {"user":"user created successfully"}


@app.get("/")
def get_user():
    users = user_service.get_user()
    return users

@app.get("/user/{user_id}")
def get_user_by_id_(user_id):
    user = user_service.get_user_by_id(user_id)
    return user

@app.put("/update_user")
def update_user_name():
    user = user_service.update_user(1,'Suleman SHEIKH')
    return {user:"user updated successfully"}

@app.delete("/user_delete")
def delete_user():
    user_service.delete_user(2)
    return {"user":"delete the user successful"}