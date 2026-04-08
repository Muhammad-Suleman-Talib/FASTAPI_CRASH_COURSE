from fastapi import APIRouter


app = APIRouter(prefix="/pro", tags=["User Management"],responses={404: {"description": "Not found"}})


@app.get("/user")
async def get_user():
    return {"message": "This is the user Router ok  endpoint"}
