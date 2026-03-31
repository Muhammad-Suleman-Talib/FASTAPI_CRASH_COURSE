from typing import Annotated

from sqlmodel import create_engine,Session,SQLModel
import os 
from fastapi import Depends

Base_db = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(Base_db)

db_path = os.path.join(Base_db,"sqlite.db")

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL,echo=True,connect_args={"check_same_thread": False})

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        
        yield session



SessionDep = Annotated[Session,Depends(get_session)]