from fastapi import FastAPI
from router import router
from user.router import app as user_router
from products.route import app as products_router
app = FastAPI(title="My API", description="This is a sample API built with FastAPI", version="1.0.0")

# @app.get("/")
# async def read_data():
#   return {"message": "Hello, World!"}

# @app.get("/student/{stu_id}")
# async def student(stu_id: int):
#   return {"Student Id": stu_id}


# @app.get("/price/{with_pri}")
# async def price(with_pri: float):
#   return {"your winning price is ": with_pri}

app.include_router(router)  # Include the router from router.py
app.include_router(user_router)  # Include the router from router.py
app.include_router(products_router)
