from fastapi import HTTPException
from app.user.model import User
from sqlmodel import select
from app.db.config import SessionDep

def create_user(name:str,email:str,session:SessionDep):
    user = User(name=name,email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"User successfully created!":user}


def get_user(session:SessionDep):
    user = session.exec(select(User)).all()
    if not user:
        raise HTTPException(status_code=404,detail="User not found!")
    return user

def delete_user(u_id:int,session:SessionDep):
    user = session.get(User,u_id)
    if not user:
        raise HTTPException(status_code=404,detail="you user with this id not found kindly put correct ID!")

    session.delete(user)
    session.commit()
    session.refresh(user)
    return {"User successfully Deleted!":user}    