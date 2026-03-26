from schemas import *
from db import create_tables
from fastapi import FastAPI,Depends
from sqlmodel import Session
from schemas import *
from services import *
from typing import List
from model import *
from db import get_session
create_tables()



app = FastAPI(title="Welcom to the fastapi where you learn modern Fastapi and Sqlmodel!")

@app.post("/create_user")
def user(name:str,email:str,cnic:int,session:Session = Depends(get_session)):
    user =  create_user(session,name=name,email=email,cnic=cnic)
    return user

@app.get("/",response_model=List[User_res])
def get_Users(session:Session=Depends(get_session)):
    get_all = get_all_users(session)
    return get_all


# @app.get("/user/{user_id}")
# def get_user_id(user_id:int):
#     user = get_User_by_id(user_id)
#     return user


# @app.put("/udpate_user")
# def update_users(up_user:Update_user):
#     user = update_user(up_user)
#     return user

# @app.patch("/zero_update")
# def patch_up(up_Update:Patch_User):
#     user = patch_user(up_Update)
#     return user


# @app.delete("/delete_user")
# def delete_us(user_id:int):
#     delete_user = delete_User(user_id)
#     return delete_user
    