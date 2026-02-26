<!-- # Fastapi with the Async configration of sqlalchemy or alembic

# first we activate the virtual environment 
# second we intall the Async sqlalchemy  go to the sqlalchemy.org and see in this **ORM Quick start** click this now you see in left side menu you see the ORM extension click this than you see first Asyncronous io
# now first you install the Async sqlalchemy using this command **pip install sqlalchemy[asyncio]**
# now i setup of sqlite setup because sql by default not support the Async support so i use the driver to **pip install aiosqlite**
# now i setup the Async alembic ok first we install the alembic aysnc first go the **alembic.sqlalchemy.org** you see the menu in the left side you click on the **cookbook** and if you click this you see on the wright side few menu option you scroll and see the use **using asyncio alembic**

# i install the alembic than init the alembic to configration in my project alembic init -t async alembic

# now you setting in the env.py file do setting change the metadat and add the render_batch_as=True ok and also change in alembic.ini file change the database link 

# if you change now you make the db folder and inside the db folder you make the file base.py and config.py 

# config.py file you import the from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker 

# than create engine and async_session ok 

# base.py in this file you import from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.asyncio import AsyncAttrs
# class Base(Async_attars, DeclarativeBase):
#      pass

# and in last import the model which you make ok 


# now we do configration and installment complete 

# now we make the first model of the user ok 

# first we create the folder in the app called user in the user folder create one model.py file to create the model 
# 1. first we need to import the base ,this is import form the sqlalchemy.orm Mapped ,and mapped_coloum and download the this import from the sqlalchemy  String 
# than create your model ok usign this import ok 

# create the services of the user like create dlete update and more

# first we create the services.py file in the user folder 
# first create the user usign 
# code also write in the file ok 

# and use the service.py file in the main.py file  -->

# 🚀 FastAPI + Async SQLAlchemy + Async Alembic — Complete Setup Guide

A production-ready guide to configure FastAPI with:

* ✅ Async SQLAlchemy
* ✅ Async Alembic
* ✅ SQLite (aiosqlite)
* ✅ Clean Architecture

---

# 📦 1. Create & Activate Virtual Environment

```bash
python -m venv venv
```

### ▶ Activate

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

# 📦 2. Install Dependencies

```bash
pip install fastapi uvicorn
pip install sqlalchemy[asyncio]
pip install aiosqlite
pip install alembic
```

---

# 🧠 Why `aiosqlite`?

SQLite async support by default nahi deta
➡ Is liye async driver use hota hai.

---

# 📁 3. Project Structure (Industry Standard)

```
app/
│
├── core/
│   └── config.py
│
├── db/
│   ├── base.py
│   └── session.py
│
├── models/
│   └── user.py
│
├── schemas/
│   └── user.py
│
├── services/
│   └── user_service.py
│
├── api/
│   └── user_routes.py
│
└── main.py
```

---

# ⚙️ 4. Database Configuration

## 📄 `db/session.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)
```

---

# 🏗 5. Base Class

## 📄 `db/base.py`

```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass
```

---

# 🔄 6. Initialize Async Alembic

```bash
alembic init -t async alembic
```

---

## ✏️ Edit `alembic/env.py`

### Import Base

```python
from app.db.base import Base
target_metadata = Base.metadata
```

### SQLite ke liye

```python
render_as_batch=True
```

---

## ✏️ Edit `alembic.ini`

```ini
sqlalchemy.url = sqlite+aiosqlite:///./test.db
```

---

# 👤 7. Create First Model

## 📄 `models/user.py`

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
```

---

# 🧬 8. Run Migration

```bash
alembic revision --autogenerate -m "create user table"
alembic upgrade head
```

---

# 🧠 9. Service Layer (Database Logic)

## 📄 `services/user_service.py`

```python
from app.db.session import AsyncSessionLocal
from app.models.user import User

async def create_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        user = User(name=name, email=email)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
```

---

# 🌐 10. API Layer

## 📄 `api/user_routes.py`

```python
from fastapi import APIRouter
from app.services.user_service import create_user

router = APIRouter()

@router.post("/users")
async def create_user_api():
    return await create_user("Suleman", "test@gmail.com")
```

---

# ▶ 11. Main File

## 📄 `main.py`

```python
from fastapi import FastAPI
from app.api.user_routes import router

app = FastAPI()

app.include_router(router)
```

---

# 🔁 Request Flow

```
Client → Route → Service → Database
```

---

# ⚡ Async Flow (Simple)

Sync:

```
Request 1 → wait → Request 2
```

Async:

```
Request 1 → waiting
            ↳ Request 2 runs
```

🚀 High performance

---

# 🧩 Architecture Explanation (Roman Urdu)

### 🏗 Model

Yahan database ki table banti hai.

### ⚙ Service

Yahan business logic hota hai
(DB create, update, delete).

### 🌐 Route

Yahan client ki request handle hoti hai.

---

# ⭐ Best Practices (Production Level)

✅ Route me DB logic na likho
✅ Service layer use karo
✅ Schema validation use karo
✅ Dependency injection use karo
✅ Environment variables use karo

---

# 🔥 Next Steps

You should now implement:

* [ ] Create user
* [ ] Get all users
* [ ] Get user by ID
* [ ] Update user
* [ ] Delete user

---

# 🏁 Run Server

```bash
uvicorn app.main:app --reload
```

---

# ❤️ Final Result

You now have:

✔ Async FastAPI
✔ Async SQLAlchemy
✔ Async Alembic
✔ Clean scalable structure
✔ Production-ready foundation

---

# 🧠 Your Learning Level

This setup = **industry standard backend architecture**

Perfect for:

* Large projects
* Team work
* Microservices
* Full-stack integration

---

# 🚀 Coming Next (Recommended)

* Dependency Injection for DB session
* Generic CRUD base
* Repository pattern
* PostgreSQL async setup
* Docker support

---
