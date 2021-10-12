import pytest
from app import create_app
from app.config import Testing
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


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
        id='test-id',
        title='test-dataset-title',
        url='http://local.dev',
        description='test-dataset-description',
        es_orga_sp=1,
        es_orga_followers=1,
        es_dataset_views=1,
        es_dataset_followers=1,
        es_dataset_featured=1,
        es_concat_title_org='test-dataset-title orga',
        logo='logo.png',
        organization_id='orga-id',
        organization='orga'
    )


@pytest.fixture
def search_client(single_dataset):
    class TestSearchClient(SearchClient):
        def clean_index(self, index):
            pass

        def index_dataset(self, to_index):
            pass

        def query_datasets(self, query_text, offset, page_size):
            return 3, [single_dataset, single_dataset, single_dataset]

        def find_one(self, dataset_id):
            return single_dataset

    return TestSearchClient()
