from unittest import mock


def test_index(app, client, single_dataset):
    dataset_service = mock.Mock()
    dataset_service.search.return_value = (1, [single_dataset])

    with app.container.dataset_service.override(dataset_service):
        response = client.post('/', content_type='multipart/form-data', data={'query': 'test'})

    assert response.status_code == 200
    assert single_dataset.title in response.data.decode()
    assert single_dataset.description in response.data.decode()
    assert single_dataset.url in response.data.decode()
