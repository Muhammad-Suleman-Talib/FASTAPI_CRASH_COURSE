from pydantic import BaseModel , Field
from typing import Annotated , Optional

class C_note(BaseModel):
    title:str
    content:str

class Up_note(BaseModel):
    id:int
    title:str
    content:str

class NotePatchUpdate(BaseModel):
    """Model for partial note updates (PATCH requests)"""
    
    # Option 1: Using typing.Optional (works in all Python versions)
    id: Optional[int] = Field(default=None, gt=0, le=1000, title="ID of the note")
    title: Optional[str] = Field(default=None, title="Title of the note")
    content: Optional[str] = Field(default=None, title="Content of the note")