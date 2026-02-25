from app.user.model import User
from app.db.config import LOCAL_SESSION
from sqlalchemy import select


def create_user(name:str,email:str,phone_no:int):
    with LOCAL_SESSION() as session:
        user = User(name=name,email=email,phone_no=phone_no)
        session.add(user)
        session.commit()


def get_user():
    with LOCAL_SESSION() as session:
        stmt = select(User)
        users = session.scalars(stmt)
        return users.all()

def get_user_by_id(user_id):
    with LOCAL_SESSION() as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalars(stmt).one_or_none()
        return user

def update_user(user_id:int,new_name:str):
    with LOCAL_SESSION() as session:
        user = session.get(User,user_id)

        if user:
            user.name = new_name
          
        session.commit()
        # session.refresh(user)
        return user

def delete_user(user_id:int):
    with LOCAL_SESSION() as session:
        user  = session.get(User,user_id)

        if user:
            session.delete(user)
            session.commit()
            return user