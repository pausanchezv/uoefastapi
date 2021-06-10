import pytest
from sqlalchemy_utils import database_exists, drop_database, create_database
from starlette.testclient import TestClient

from app.core.settings import get_settings
settings = get_settings()
settings.activate_testing_database()

from app.core.database import Base, engine
from app.main import app


@pytest.fixture(scope="class", autouse=True)
def create_test_database():
    """
    Creates a clean testing database on every test class.
    Scope=class so that a database lasts an entire class and the objects created by the setup method will
    persist all the tests of that class. Then the tearDown method will drop the database and get ready for
    the next test.
    """
    if database_exists(settings.database_url_test):
        drop_database(settings.database_url_test)
    create_database(settings.database_url_test)
    Base.metadata.create_all(engine)

    # Run the tests
    yield

    drop_database(settings.database_url_test)


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases
    """
    with TestClient(app) as client:
        yield client
