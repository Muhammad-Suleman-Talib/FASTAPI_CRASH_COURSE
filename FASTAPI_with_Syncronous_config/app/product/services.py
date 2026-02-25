from app.db.config import LOCAL_SESSION
from app.product.model import Product
from sqlalchemy import select

def create_product(product_name:str,category:str,price:int,stock:int):
    with LOCAL_SESSION() as session:
        product = Product(product_name=product_name,category=category,price=price,stock=stock)
        session.add(product)
        session.commit()