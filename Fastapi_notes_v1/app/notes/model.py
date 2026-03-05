from pickle import TRUE

from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Text

class Notes(Base):
    __tablename__="notes"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String,nullable=False)
    content:Mapped[str] = mapped_column(Text)
