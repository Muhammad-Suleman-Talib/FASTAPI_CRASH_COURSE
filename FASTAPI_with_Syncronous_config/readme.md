# Project Title >::  fastapi with syncronous setting with the sqlalchemy or alembic migration 
# 1. first we do to activate the virtual environment 
## 2 .second we install the fastapi using this command **_fastapi[standard]_**
## 3. than create the **.gitignore_file and add the files which we not share**
## 4. make the requirements.txt file 

## 5. create the app folder and make the main.py file 
## 6 we use the Sqlalchemy or alemibic 

## to add the sqlalchemy to work with the syncronous way how to deal with the syncronous programming ok 

## first we go to this **https://docs.sqlalchemy.org/** in this we see current document section in this seciton we go to the installation guide i click this in this we found the command how to install this usign this command **pip install SQLAlchemy**

# after the installation we make the main.py file in this file we do all the fastapi related operation  than we make the db folder in this we create first the __init__.py file which make this folder into the package ok create one config.py to create the database

# in the config.py file  we do first import the **from sqlalchemy import create_engine**
# secon we use the sessionmaker for session **from sqlalchemy.orm import sessiomaker**

# next i create the another file base.py in this file i make the base class for the to make tables of the sqlalchemy usying the alembic 

# base.py file we import first ** from sqlalchemy.orm import DeclarativeBase**

# now we install the alembic frist we go to this site **https://alembic.sqlalchemy.org/** in this link we hit than we see the frontmatter i click this than see all the usage ok 

# SETUP OF THE SQLALCHEMY OR ALEMBIC GUIDE FOR BEGINERS

# first we install the alembic using the this command **pip install alembic**
# after installation we setup this in my project usign this command  **alembic init alembic ** if i hit this than you see one project of alembic create in our project floder name **alembic** in this folder you see the version folder inside this version folder all the version of migration come ... and you see the alembic.ini file where you set the few things first go change this settion ok **sqlalchemy.url = driver://user:pass@localhost/dbname **add in this own database url ok change this its first setting and second you go to the env.py file in this file you change the **target_metadata = None** you change this add your own metadata using the Base.metadata class ok this is the another setting render_as_batch=True in the online connection in connection.connect  

# now we make the first model i use the folder structure same like django easy to share structure ok first we make the user folder in this i do all the user related work ok ...
# i created the folder user in the user i make the file model.py in this file i create the model using the sqlachemy.orm import the Mapped and mapped_coloum and import the base class and sqlalchemy import String ok 

# kingly first your model import in the base class or parent class if you not import than you do not autogenerate the model ok ...
# after creating the model now we use the alembic to create the talbe in the database 
# first we do to run the alembic command : ....
# alembic revision --autogenerate -m "create user table"
# alembic upgrade head 

# i create one user table one product table now we add the data in this table...
# after creation of the talbe i add the data in this first i create the services .py file in all the folder like the user , product 


# in the service.py file we do the crud operatin to see how i add the data ok 
# first i import the model which model i make 
# second we import the session local session i created 
# third we import the from sqlalchemy import the select...

# if we like to create the model like to add the data like login or user related or product related ok 

# 1 : with local_session() as session:
# 2 user=  User(name=name,email=email)
# 3  session.add(user)
# 4 session.commit()


# if wwe like to see all the data so i use the scalrs

# first line same for all ok 
# second we make the stmt = select(User)
# user = session.scalars(stmt)
# return user.all()


# if you want the data come acc to the id of the user if you like this type so its simple 

# first line same for all ok 
# second we make the stmt = select(User).where(User.id == you take in this id in the function like user_id)
# user = session.scalars(stmt).one_or_none()
# return user

# HOW TO MAKE THE UPDATE FUNCTION TO UPDATE THE DATA OF THE USER 

# # 🚀 FastAPI + Synchronous SQLAlchemy + Alembic — Complete Beginner Guide

A production-style backend setup using **FastAPI**, **SQLAlchemy (Sync)** and **Alembic Migration** with a clean architecture.

---

# 📖 What is FastAPI?

**FastAPI** is a modern, high-performance Python web framework used to build APIs.

### ✅ Why FastAPI?

* Very fast (based on Starlette & Pydantic)
* Automatic Swagger docs
* Type hint support
* Easy to learn
* Production ready

---

# 🗄 What is SQLAlchemy?

**SQLAlchemy** is a Python ORM (Object Relational Mapper).

### ✅ Why SQLAlchemy?

* Convert Python classes → Database tables
* Write Python instead of raw SQL
* Powerful querying system
* Database independent

---

# 🔄 What is Alembic?

**Alembic** is a database migration tool for SQLAlchemy.

### ✅ Why Alembic?

* Create tables automatically
* Modify tables safely
* Version control for database
* Production standard migrations

---

# ⚙️ Step 1 — Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

# ⚙️ Step 2 — Install FastAPI

```bash
pip install "fastapi[standard]"
```

---

# ⚙️ Step 3 — Create `.gitignore`

```gitignore
venv/
__pycache__/
.env
alembic/versions/
```

---

# ⚙️ Step 4 — Create requirements.txt

```bash
pip freeze > requirements.txt
```

---

# 🗂 Project Folder Structure

```
app/
 ├── main.py
 ├── db/
 │    ├── __init__.py
 │    ├── config.py
 │    └── base.py
 ├── user/
 │    ├── model.py
 │    └── service.py
```

---

# 🧠 Synchronous Programming (Concept)

Synchronous ka matlab:

➡ Code line by line execute hota hai
➡ Next line tab chalegi jab DB response complete ho
➡ Simple & beginner friendly

---

# 🗄 Database Configuration

## 📄 db/config.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=True)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
```

---

# 🧱 Base Class for All Models

## 📄 db/base.py

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

---

# 🔄 Alembic Installation

```bash
pip install alembic
alembic init alembic
```

---

## ⚙️ alembic.ini

```ini
sqlalchemy.url = sqlite:///./test.db
```

---

## ⚙️ alembic/env.py

```python
from app.db.base import Base
target_metadata = Base.metadata
```

---

# 👤 Create First Model

## 📄 user/model.py

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
```

⚠ Important: Model must be imported so Alembic can detect it.

---

# 🔄 Run Migration

```bash
alembic revision --autogenerate -m "create user table"
alembic upgrade head
```

---

# 🧩 CRUD Operations (Service Layer)

## ➕ Create User

```python
def create_user(name, email):
    with LocalSession() as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
```

---

## 📖 Get All Users

```python
from sqlalchemy import select

def get_all_users():
    with LocalSession() as session:
        stmt = select(User)
        users = session.scalars(stmt)
        return users.all()
```

---

## 🔍 Get User By ID

```python
def get_user_by_id(user_id: int):
    with LocalSession() as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalars(stmt).one_or_none()
        return user
```

---

## ✏️ Update User

```python
def update_user(user_id: int, name: str, email: str):
    with LocalSession() as session:

        stmt = select(User).where(User.id == user_id)
        user = session.scalars(stmt).one_or_none()

        if not user:
            return None

        user.name = name
        user.email = email

        session.commit()
        session.refresh(user)

        return user
```

---

## ❌ Delete User

```python
def delete_user(user_id: int):
    with LocalSession() as session:

        user = session.get(User, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        return True
```

---

# 🌐 FastAPI Main File

## 📄 main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI with Sync SQLAlchemy"}
```

---

# ▶️ Run the Project

```bash
uvicorn app.main:app --reload
```

---

# 🌟 Features of This Architecture

✅ Clean & scalable structure
✅ Service layer pattern
✅ Proper migration system
✅ ORM based database handling
✅ Beginner → Production ready

---

# ❤️ Summary

This setup provides:

* FastAPI for API creation
* SQLAlchemy for database ORM
* Alembic for migrations
* Synchronous execution for simplicity

Perfect for real-world backend development and learning clean architecture.
