from app.db.config import Async_session
from app.notes.model import *
from sqlalchemy import select
from app.notes.schemas import *
from fastapi import HTTPException

async def create_note(notes:C_note):
    async with Async_session() as session:
        note = Notes(title=notes.title,content=notes.content)
        session.add(note)
        await session.commit()
        return {"status":"you successfully create the Note!"}
    
async def get_note():
    async with Async_session() as session:
        stmt = select(Notes)
        note = await session.scalars(stmt)
        return note.all()
    
async def get_note_by_id(note_id:int):
    async with Async_session() as session:
        note = await session.get(Notes,note_id)
        if not note:
            raise HTTPException(status_code=404,detail="your note id is incorrect")
        return note
    
async def update_note(update_note:Up_note):
    async with Async_session() as session:
        note = await session.get(Notes,update_note.id)

        if not note:
            raise HTTPException(status_code=404,detail="your Note id is incorrect!")
        note.title = update_note.title
        note.content = update_note.content
        await session.commit()
        await session.refresh(note)
        return {"updated Note":note}
    
async def patch_update(patch_update:NotePatchUpdate):
    async with Async_session() as session:
        note = await session.get(Notes,patch_update.id)
        if not note:
            raise HTTPException(status_code=404,detail="YOur Note id is incorrect kindly add the correct id!")
        if patch_update.title is not None:
            note.title = patch_update.title
        if patch_update.content is not None:
            note.content = patch_update.content

        await session.commit()
        await session.refresh(note)
        return {"Patch Note" : note}


async def delete_note(note_id:int):
    async with Async_session() as session:
        note = await session.get(Notes,note_id)
        if not note:
            raise HTTPException(status_code=404,detail="Your note Id is incorrect!")
        await session.delete(note)
        await session.commit()
        return {"Delete Note" : note}                        
        

        
        

 
