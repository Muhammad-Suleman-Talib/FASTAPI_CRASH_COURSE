from typing import Annotated, List


from fastapi import FastAPI,Depends, HTTPException, Header


from service import toke_verify
from router import routers

app = FastAPI(title="Dependency Injection",dependencies=[Depends(toke_verify)])

# async def user_name(name:str):
#     return name


# def user_profile(role:list[str],age:int,name:str=Depends(user_name)):
#     return {"name":name,"age":age,"role":role}


# # Depends  funciton is use to inject the dependency into you endpoint its first check and run all the dpendencies than its run the endpoint and return the response
# @app.post('/')
# async def get_data(profile:dict=Depends(user_profile)):
#     return profile


fruits_list = ["appple","banana","grapes","orange"]


def get_list(fruits:List[str]):

    return fruits

print(get_list(fruits_list))

def get_f(fruits:List[str]):

    yield fruits

get_f(fruits_list)


def test():
    print("test function")
    yield 1
    print("2nd function after yield")
    yield 2
    print("3rd function after yield")
    yield 3

t = test()
print(next(t))
print(next(t))
print(next(t))




app.include_router(routers)
