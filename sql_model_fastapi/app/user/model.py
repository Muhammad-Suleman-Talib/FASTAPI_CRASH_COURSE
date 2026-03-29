from sqlmodel import SQLModel,Field

class User(SQLModel,table=True):
    id:int = Field(primary_key=True)
    name:str = Field(nullable=False)
    email:str = Field(nullable=False , unique=True)

    def __repr__(self):
        return f"<User(name={self.name} email={self.email})>"
    