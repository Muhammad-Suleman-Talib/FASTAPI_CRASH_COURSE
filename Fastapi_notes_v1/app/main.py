from fastapi import FastAPI 
from app.notes.schemas import *
from app.notes import services as note_services




app = FastAPI(title="Welcome to the world of Fastapi where you learn modern Api's development!")

@app.post("/create_note")
async def create_note(note:C_note):
    create_note = await note_services.create_note(note)
    return create_note

@app.get("/")
async def get_note():
    get_all_note = await note_services.get_note()
    return get_all_note

@app.get("/note/{note_id}")
async def get_note_by_id(note_id:int):
    get_notes = await note_services.get_note_by_id(note_id)
    return get_notes

@app.put("/update_note")
async def update_note(note:Up_note):
    update_note = await note_services.update_note(note)
    return update_note

@app.patch("/patch_note")
async def patch_note(patch_note:NotePatchUpdate):
    patch_Note = await note_services.patch_update(patch_note)
    return patch_Note

@app.delete("/delete_note")
async def delete_note(note_id:int):
    delete_note = await note_services.delete_note(note_id)
    return delete_note