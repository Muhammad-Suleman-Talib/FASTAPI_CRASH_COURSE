
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker,AsyncSession

import os 
from fastapi import Depends
from typing import Annotated

Base_Dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(Base_Dir,"this is the path")

Base_path = os.path.join(Base_Dir,"sqlite.db")
DATA_BASE_URL = f"sqlite+aiosqlite:///{Base_path}"

engine = create_async_engine(DATA_BASE_URL,echo=True)

Async_session = async_sessionmaker(bind=engine,expire_on_commit=False)

# this is for the production ok i use this code for the prodution 
# async def get_db():
#     async with Async_session() as session:
#         yield session


# now we like to see the session is created or not check this using this code in development ok 

async def get_db():
    session = Async_session()
    print(f"session is created {id(session)}")
    try:
        async with session:
            yield session
        print(f"Session commited and close {id(session)}")
    except Exception as e:
        print(f"Error in session {id(session)} Rolling back {str(e)}")
        await session.rollback()
        
    finally:
        await session.close()
        print(f"Session is close {id(session)}")    


Session_Dep = Annotated[AsyncSession,Depends(get_db)]        