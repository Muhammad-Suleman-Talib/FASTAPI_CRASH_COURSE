from typing import List, Annotated
from fastapi import Header, HTTPException


async def toke_verify(token:Annotated[str,Header()]):
    if token != "my-secret-toke":
        raise HTTPException(status_code=401,detail="Invalid token")
    return token



class Test():
    def __init__(self,name,email) -> None:
        self.name = name
        self.email = email
    @staticmethod
    def profile(role,sallary):
        return {"role":role,"sallary":sallary}

mytesting = Test("John Doe","suleman@gmail.com")
myprofile = Test.profile(role="Developer",sallary="1000$")

