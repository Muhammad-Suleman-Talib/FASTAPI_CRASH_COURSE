from pydantic import BaseModel
class User_res(BaseModel):
    id:int
    name:str
    email:str
    cnic:int 


class Update_user(BaseModel):
    id:int
    name:str    
    email:str
    cnic:int

class Patch_User(BaseModel):
    id:int
    name:str  | None=None  
    email:str| None=None  
    cnic:int| None=None  