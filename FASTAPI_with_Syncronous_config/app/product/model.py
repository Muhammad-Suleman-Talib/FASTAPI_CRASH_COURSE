from sqlalchemy.orm import Mapped ,mapped_column
from app.db.base import Base
from sqlalchemy import String


class Product(Base):
    __tablename__="product"
    id:Mapped[int] = mapped_column(primary_key=True)
    product_name:Mapped[str] = mapped_column(String(20),nullable=False)
    category:Mapped[str] = mapped_column(String(20),nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    stock:Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Product(id= {self.id} product name {self.product_name} category {self.category} price {self.price} stock {self.stock} )>"

