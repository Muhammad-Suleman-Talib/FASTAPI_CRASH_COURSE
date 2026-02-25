from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.user import model
from app.product import model