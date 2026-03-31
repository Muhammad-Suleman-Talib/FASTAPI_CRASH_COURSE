from sqlmodel import SQLModel,Field


class Task(SQLModel,table=True):
    id:int = Field(primary_key=True,index=True)
    title:str = Field(nullable=False,index=True,unique=True)
    content:str  = Field(nullable=False)
