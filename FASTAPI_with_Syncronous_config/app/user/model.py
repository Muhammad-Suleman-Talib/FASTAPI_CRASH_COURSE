from sqlalchemy.orm import Mapped , mapped_column
from app.db.base import Base
from sqlalchemy import String, Integer


class User(Base):
    __tablename__="users"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20),nullable=False)
    email:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    phone_no:Mapped[int] = mapped_column(unique=True,nullable=False)

    def __repr__(self):
        return f"<User(id={self.id} name={self.name} email={self.email} phone number {self.phone_no})>"
    