from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Verifica que NO haya espacios extra ni errores en esta línea:
SQLALCHEMY_DATABASE_URL = "postgresql://carlos:password123@127.0.0.1:5433/dashai_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()