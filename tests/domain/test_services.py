from unittest import mock
from app.domain.interfaces import SearchClient
from app.domain.services import DatasetService


def test_dataset_service_call(single_dataset):
    search_client = SearchClient
    search_client.index = mock.MagicMock(return_value=None)
    search_client.query_datasets = mock.MagicMock(return_value=(0, []))

    dataset_service = DatasetService(search_client=search_client)

    dataset_service.feed(single_dataset)
    search_client.index.assert_called()

    results, results_number, total_pages = dataset_service.search('test', 1, 20)
    search_client.query_datasets.assert_called()
    assert results == []
    assert results_number == 0
    assert total_pages == 1


def test_dataset_service_search(single_dataset):
    search_client = SearchClient
    search_client.query_datasets = mock.MagicMock(return_value=(3, [single_dataset, single_dataset, single_dataset]))

    dataset_service = DatasetService(search_client=search_client)

    results, results_number, total_pages = dataset_service.search('test', 1, 20)
    search_client.query_datasets.assert_called()
    assert len(results) == 3
    assert results_number == 3
    assert total_pages == 1


def test_dataset_service_find_one(single_dataset):
    search_client = SearchClient
    search_client.find_one = mock.MagicMock(return_value=single_dataset)

    dataset_service = DatasetService(search_client=search_client)

    result = dataset_service.find_one('test_id')
    search_client.find_one.assert_called()
    assert result.title == single_dataset.title
    assert result.description == single_dataset.description
    assert result.id == single_dataset.id
    assert result.url == single_dataset.url
