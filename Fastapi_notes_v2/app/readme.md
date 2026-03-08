# 1. pip install fatapi[standard]
# 2 pip install sqlalchemy[asyncio]
# 3 pip install alembic
# 4 pip install aiosqlite
# 5 alembic init -t async alembic
# 6 alembic revision --autogenerate -m "create the table"
# 7 alembic upgrade head  