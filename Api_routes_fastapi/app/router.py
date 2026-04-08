from fastapi import APIRouter

router = APIRouter()


@router.get("/hello",tags=["hello"])
async def router_test():
    return {"message": "Hello from the router!"}

