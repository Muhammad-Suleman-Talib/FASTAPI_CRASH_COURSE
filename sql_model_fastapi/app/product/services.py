
from fastapi import HTTPException
from app.product.model import Product
from app.db.config import SessionDep
from sqlmodel import select

def create_product(session:SessionDep,p_name:str,price:int):
    product = Product(product_name=p_name,price=price)
    session.add(product)
    session.commit()
    session.refresh(product)
    return {"product created successfully!":product}

def get_product(session:SessionDep):
    product = session.exec(select(Product)).all()
    if not product:
        raise HTTPException(status_code=404,detail="you product not found!")
    
    return product


def get_product_id(session:SessionDep,product_id:int):
    product = session.get(Product,product_id)
    if not product_id:
        raise HTTPException(status_code=404,detail="the product with this id not show!")
    
    return product


def update_product(session:SessionDep,product_id:int,update_p_name:str,u_price:int):
    product = session.get(Product,product_id)
    if not product:
        raise HTTPException(status_code=404,detail="you product id not match!") 
    if product:
        product.product_name =   update_p_name
        product.price = u_price

    session.commit()
    session.refresh(product)
    return product    


def delete_product(session:SessionDep,pro_id:int):
    product = session.get(Product,pro_id)
    if not product:
        raise HTTPException(status_code=404,detail="you product id not match!")
    session.delete(product)
    session.commit()
    session.refresh(product)
    return product