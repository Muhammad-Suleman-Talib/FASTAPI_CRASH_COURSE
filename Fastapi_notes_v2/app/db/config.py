from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import os 

Dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base_paht = os.path.join(Dir_path,"sqlite.db")

DATABASE_URL = f"sqlite+aiosqlite:///{Base_paht}"
engine = create_async_engine(DATABASE_URL,echo=True)

Async_session = async_sessionmaker(bind=engine,expire_on_commit=False)
