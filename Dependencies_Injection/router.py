from fastapi import APIRouter, Depends
from service import toke_verify,myprofile,mytesting,Test

routers = APIRouter(
)


@routers.get("/hello", tags=["hello"])
async def router_test():
    return {"message": "Hello from the router!"}


@routers.post("/test")
async def get_testing(user:str = Depends(Test),role:str = Depends(Test.profile)):
    return {"user":user,"role":role}

@routers.get("/test")
async def gettest():
    return {"user":mytesting,"profile":myprofile}
