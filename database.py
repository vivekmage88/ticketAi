import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), pool_size = 20, max_overflow = 10)
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

