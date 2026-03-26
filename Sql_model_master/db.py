from sqlmodel import create_engine,SQLModel,Session

DATA_BASE_URL = "sqlite:///sqlite.db"

engine = create_engine(DATA_BASE_URL,echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session