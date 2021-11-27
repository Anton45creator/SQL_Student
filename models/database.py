from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'application.db'
engine = create_engine(f'PostgreSQL:///{DATABASE_NAME}')
Session = sessionmaker(band=engine)

Base = declarative_base


def create_db():
    Base.metadata.create_all(engine)
