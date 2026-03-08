from app.db.base import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String,DateTime,Text
from datetime import datetime,timezone

class Notes(Base):
    __tablename__="notes"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    content:Mapped[str] = mapped_column(Text,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.now(timezone.utc),nullable=False,index=True)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False,)
    
    def __repr__(self):
        return f"<Notes(id={self.id} name={self.name} created at {self.created_at})>"