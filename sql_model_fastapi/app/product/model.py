
from sqlmodel import SQLModel,Field

class Product(SQLModel,table=True):
    id:int = Field(primary_key=True,index=True)
    product_name:str = Field(nullable=False)
    price:int = Field(nullable=False)