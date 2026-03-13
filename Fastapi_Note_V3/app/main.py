from typing import List

from fastapi import FastAPI
from app.db.config import Session_Dep
from app.notes import services as note_service
from app.notes.schemas import *
app = FastAPI(title="WELCOME TO THE WORLD OF THE FASTAPI!")

# different way to do the sqlalchemy or session in this ok 
# @app.post("/create_note",response_model=Note_out)
# async def create_note(note:Create_note,session:AsyncSession=Depends(get_db)):
#     note = await note_service.create_note(note)
#     return note

@app.post("/create_note",response_model=Note_out)
async def create_note(session:Session_Dep,note:Create_note):
    note = await note_service.create_note(session,note=note)
    return note

@app.get("/",response_model=List[Note_out])
async def get_all_notes(session:Session_Dep):
    note = await note_service.get_note(session)
    return note


@app.get("/note/{note_id}")
async def get_note_by_id(session:Session_Dep,note_id:int):
    note = await note_service.get_note_by_id(session,note_id)
    return note 



@app.put("/update_note",response_model=Note_out)
async def update_note(session:Session_Dep,update_notes:Update_note):
    up_note = await note_service.update_note(session,update_note=update_notes)
    return up_note


@app.patch("/patch_update")
async def patch_update(session:Session_Dep,patch_update:Patch_update):
    note = await note_service.patch_update(session,patch_note=patch_update)
    return note 

@app.delete("/delete_note")
async def delete_note(session:Session_Dep,user_id:int):
    note = await note_service.delete_note(session,user_id)
    return note 