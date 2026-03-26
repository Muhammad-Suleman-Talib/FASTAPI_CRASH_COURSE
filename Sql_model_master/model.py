from token import OP
from typing import List, Optional

from sqlmodel import Field,SQLModel,Relationship


class UserAddressLink(SQLModel,table=True):
    user_id:int = Field(foreign_key="users.id",primary_key=True)
    address_id:int = Field(foreign_key="address.id",primary_key=True)

class Users(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str = Field(title='Enter you correct Name ',nullable=False)
    email:str = Field(title="enter you email",unique=True,nullable=False)
    password:int = Field(title="enter The strong password",nullable=False)
    # product:List["Product"] = Relationship(back_populates="users")

#category 

# class Category(SQLModel,table=True):
    # id:Optional[int] = Field(default=None, primary_key=True)
    # category_name:str = Field(title="enter the category name ")
    # products:List["Product"] = Relationship(back_populates="category")
    

    
# one to many  
# class Product(SQLModel,table=True):
    # id:int = Field(default=None,primary_key=True)
    # category_id:Optional[int] = Field(foreign_key="category.id"  )
    # product_name:str = Field(title="Enter your Bio title")
    # product_image:str = Field(title="add the product image url")    
    # product_price:str = Field(title="Enter the product price") 
    # category:Optional["Category"] = Relationship(back_populates="product")   



# class Address(SQLModel,table=True):
    # id:Optional[int] = Field(default=None,primary_key=True)
    # street:str = Field(title="Enter you correct address with the street name and closest place ")
    # city:str = Field(title="Enter you city Name")


