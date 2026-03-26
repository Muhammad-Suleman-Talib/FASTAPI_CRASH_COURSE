from sqlmodel import   select
from model import Users
from fastapi import HTTPException
from schemas import *

def create_user(session,name:str,email:str,cnic:int):
    user = Users(name=name,email=email,cnic=cnic)
    session.add(user)
    session.commit()
    session.refresh(user)
    return "User Successfully created!"


def get_all_users(session):
    stmt = select(Users)
    users = session.exec(stmt).all()
    return users
      
def get_User_by_id(session,user_id:int):
    user = session.get(Users,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="you user id not match")
    
    return user
    
def update_user(session,update_user:Update_user):
    user = session.get(Users,update_user.id)
    if not user:
        raise HTTPException(status_code=404,detail="you id not match kindly add correct id ")
    
    user.name = update_user.name
    user.email = update_user.email
    user.cnic = update_user.cnic

    session.commit()
    session.refresh(user)
    return user


def patch_user(session,pa_user:Patch_User):
    user = session.get(Users,pa_user.id)
    if not user:
        raise HTTPException(status_code=404,detail="your user id is not match kindly put correct id")
    
    if pa_user.name is not None:
        user.name = pa_user.name

    if pa_user.email is not None:
        user.email = pa_user.email

    if pa_user.cnic is not None:
        user.cnic = pa_user.cnic

    session.commit()
    session.refresh(user)
    return user    


def delete_User(session,user_id:int):
    user = session.get(Users,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="your user id is not correct kidly add corrrect id")
    
    session.delete(user)
    session.commit()
    return {"User Deleted Successfully":user}