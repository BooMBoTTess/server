import sys
sys.path.append(r'C:\pycharm\Async_dash_test')
sys.path.append(r'C:\pycharm\Async_dash_test\server_app')

from typing import Generator
from config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from server_app.app import app




@pytest.fixture(scope='session')
def db_engine():
    """Creates a fill_tables database and yields a database engine"""

    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(
        DATABASE_URL,
    )
    yield engine

@pytest.fixture(scope='function')
def db_session(db_engine):
    """Creates a connection to the fill_tables database and handles cleanup"""
    connection = db_engine.connect()
    # Begin a non-ORM transaction
    database_session = Session(bind=connection, expire_on_commit=False)
    yield database_session
    database_session.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db_session) -> Generator[TestClient, None, None]:
    """
    Надо настроить чтобы он был соеденен с игрушечной базой данных наверно
    """

    with TestClient(app) as test_client:
        yield test_client



def test_read_exist_departments(client):

    response = client.get('/auth/login')
    assert response.status_code == 200




def test_func(client):
    response = client.get('/home')
    assert response.status_code == 402
