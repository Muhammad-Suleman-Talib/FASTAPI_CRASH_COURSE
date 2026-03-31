
from fastapi import HTTPException

from app.db.config import SessionDep
from sqlmodel import select
from app.model.student_model import User


def create_user(session:SessionDep,name:str,email:str):
    user = User(name=name,email=email)
    session.add(user)
    session.commit()
    return "User Successfully created"

def get_user(session:SessionDep):
    user = session.exec(select(User)).all()
    if not user:
        raise HTTPException(status_code=404,detail="you user not found!")
    
    return user
