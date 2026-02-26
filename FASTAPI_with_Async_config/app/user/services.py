from typing import Awaitable, Optional

from app.db.config import Async_session
from app.user.model import User
from sqlalchemy import select
from pydantic import BaseModel



async def create_user(name:str,email:str):
    async with Async_session() as session:
        user = User(name=name,email=email)
        session.add(user)
        await session.commit()


async def get_user_data():
    async with Async_session() as session:
        stmt = select(User)
        user = await session.scalars(stmt)
        return user.all()
    

async def get_user_by_id(user_id:int):
    async with Async_session() as session:    
        stmt = select(User).where(User.id == user_id)
        user = await session.scalars(stmt) 
        return user.first()
    
async def update_user_name_email(user_id:int,new_name:str|None=None,new_email:str | None=None):
    async with Async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            return None
        if new_name is not None:
            user.name = new_name
        if new_email is not None:
            user.email = new_email
        await session.commit()
        return user    

async def delete_user(user_id:int):
    async with Async_session() as session:
        user = await session.get(User,user_id)
        if user:
            await session.delete(user)
            await session.commit()
        