from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE = "postgres:123456@localhost/test_db"


@fixture(scope="function", autouse=True)
def db_session():
    engine = create_engine(f'postgresql+psycopg2://{DATABASE}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
