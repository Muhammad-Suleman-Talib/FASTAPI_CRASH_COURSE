from app.db.config import SessionDep,create_tables
from app.user import services as user_services
from app.product import services as prod_services
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan,title="Welcome to the world of the fastapi where you learn complete Modern Api development study.")



@app.post("/create_user")
def create_users(name,email,session:SessionDep):
    return user_services.create_user(name,email,session)

@app.get("/users")
def get_Users(session:SessionDep):
    return user_services.get_user(session)


@app.post("/product")
def create_Product(pro_name:str,price:int,session:SessionDep):
    return prod_services.create_product(p_name=pro_name,price=price,session=session)


@app.get("/")
def get_Product(session:SessionDep):
    return prod_services.get_product(session)