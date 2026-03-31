from app.services import services as user_services
from app.db.config import SessionDep,create_table
from fastapi import FastAPI

app = FastAPI(title="hello and welcome to the fastapi master course where you learn modern orm")

create_table()

@app.post("/create_user")

def create_users(session:SessionDep,name,email):
    user = user_services.create_user(session,name,email)
    return user


@app.get("/")
def get_user(session:SessionDep):
    return user_services.get_user(session)