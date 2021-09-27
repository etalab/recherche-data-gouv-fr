import pytest
from app import create_app
from app.config import Testing
from app.domain.entities import Dataset


@pytest.fixture
def app():
    app = create_app(Testing)
    yield app
    app.container.unwire()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture
def single_dataset():
    return Dataset(
        remote_id='test-id',
        title='test-dataset-title',
        url='http://local.dev',
        description='test-dataset-description',
        featured=True
    )
