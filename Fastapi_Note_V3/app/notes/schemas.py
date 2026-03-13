from typing import Annotated, Optional

from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime

class Create_note(BaseModel):
    title:str = Field(examples=['Atomic Habits,Nelson Mandela',"pakistan"],description="enter the title of the title")
    content:str = Field(description="enter the content of the Note")

class Note_create(Create_note):
    pass

class Update_note(BaseModel):
    id:int
    title:str = Field(default="default title",examples=['Atomic Habits,Nelson Mandela',"pakistan"],description="enter the title of the title")
    content:str = Field(description="enter the content of the Note")


class Patch_update(BaseModel):
    id:int
    title:Optional[str] = Field(None,examples=['Atomic Habits,Nelson Mandela',"pakistan"],description="enter the title of the title") 
    content:Optional[str]  = Field( None, description="enter the content of the Note") 


class Note_out(BaseModel):
    id:int 
    title:str = Field(examples=['Atomic Habits,Nelson Mandela',"pakistan"],description="enter the title of the title")
    content:str = Field(description="enter the content of the Note")
    # created_at:datetime
    model_config=ConfigDict(from_attributes=True)
            

