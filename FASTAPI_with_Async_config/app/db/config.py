from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = os.path.join(BASE_DIR,"sqlite.db")
# print(BASE_DIR)
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
engine = create_async_engine(DATABASE_URL,echo=True)

Async_session = async_sessionmaker(bind=engine,expire_on_commit=False)
