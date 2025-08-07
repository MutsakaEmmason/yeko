from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

DB_USERNAME = 'root'
DB_PASSWORD = 'marvin'
DB_NAME = 'library_db'
DB_HOST = 'localhost'

DATABASE_URL = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
