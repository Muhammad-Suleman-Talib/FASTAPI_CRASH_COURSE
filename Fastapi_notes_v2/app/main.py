from typing import List

from fastapi import FastAPI
from app.notes import services as note_service
from app.notes.schemas import *
app = FastAPI(title="WELCOME TO THE WORLD OF THE FASTAPI!")

@app.post("/create_note",response_model=Note_out)
async def create_note(note:Create_note):
    note = await note_service.create_note(note)
    return note

@app.get("/all_Notes",response_model=List[Note_out])
async def get_all_notes():
    note = await note_service.get_note()
    return note


@app.get("/note/{note_id}")
async def get_note_by_id(note_id:int):
    note = await note_service.get_note_by_id(note_id)
    return note 



@app.put("/update_note",response_model=Note_out)
async def update_note(update_notes:Update_note):
    up_note = await note_service.update_note(update_note=update_notes)
    return up_note


@app.patch("/patch_update")
async def patch_update(patch_update:Patch_update):
    note = await note_service.patch_update(patch_note=patch_update)
    return note 

@app.delete("/delete_note")
async def delete_note(user_id:int):
    note = await note_service.delete_note(user_id)
    return note 