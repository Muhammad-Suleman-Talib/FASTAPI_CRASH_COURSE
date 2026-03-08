
from app.notes.model import *
from app.db.config import Async_session
from app.notes.schemas import *
from sqlalchemy import select
from fastapi import HTTPException

async def create_note(note:Create_note):
    async with Async_session() as session:
        create_Note = Notes(name=note.title,content=note.content)
        if not create_Note:
            raise HTTPException(status_code=404,detail="you note is not created you have not well data")
        
        session.add(create_Note)
        await session.commit()
        await session.refresh(create_Note)
        return {
            "id": create_Note.id,
            "title": create_Note.name,  # Important: name se title mein map kar rahe
            "content": create_Note.content,
        }
        # return {"Your Note created Successfully":response_data}
        # return create_Note
    
async def get_note():
    async with Async_session() as session:
        stmt =  select(Notes)
        note = await session.scalars(stmt)

        if not note:
            raise HTTPException(status_code=404,detail="your Note not found!")
        result = note.all()
        notes_data = []
        for notes in result:
            notes_data.append({
                "id":notes.id,
                "title":notes.name,
                "content":notes.content,
                "created_at":notes.created_at,
            })
        return notes_data

async def get_note_by_id(note_id:int):
    async with Async_session() as session:
        note = await session.get(Notes,note_id)
        if not note:
            raise HTTPException(status_code=404,detail="your note id is incorrect")
        return note

async def update_note(update_note:Update_note):
    async with Async_session() as session:
        note = await session.get(Notes,update_note.id) 
        if not note:
            raise HTTPException(status_code=404,detail="your note Id is incorrect kindly add correct id to update the NOte")
        
        note.name = update_note.title
        note.content = update_note.content
        await session.commit()
        await session.refresh(note)
        return {
            "id":note.id,
            "title":note.name,
            "content":note.content,

        }
    
async def patch_update(patch_note:Patch_update):
    async with Async_session() as session:
        note = await session.get(Notes,patch_note.id)     
        if not note:
            raise HTTPException(status_code=404,detail="your not ID is incorrect kinldy add correct id ")
        if patch_note.title is not None:
            note.name = patch_note.title
        if patch_note.content is not None:
            note.content = patch_note.content
        await session.commit()
        await session.refresh(note)
        return {"Your Note Patch Updated":note}       

async def delete_note(note_id:int):
    async with Async_session() as session:
        note = await session.get(Notes,note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Your note Id is not Match!")
        await session.delete(note)
        await session.commit()
        return {"Your Note is Deleted":note}