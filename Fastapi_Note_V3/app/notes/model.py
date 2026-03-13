from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String ,DateTime
from app.db.base import Base
from datetime import datetime
import pytz

def Pakistan_time():
    return datetime.now(pytz.timezone("Asia/Karachi"))



class Notes(Base):
    __tablename__="notes"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    content:Mapped[str] = mapped_column(nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=Pakistan_time,index=True)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=Pakistan_time,onupdate=Pakistan_time,index=True)

    def __repr__(self):
        return f"<Notes(id={self.id} name={self.name} created at {self.created_at})>"


