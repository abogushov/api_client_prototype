from ..client import APIClient


def test_api_client_context_manager(test_api_server):
    client = APIClient({}, loop=test_api_server._loop)

    with client:
        assert client.session

    assert client.session is None


def test_api_client(test_api_server):
    client = APIClient({
        'server': test_api_server.make_url(''),
        'headers': {'DATA': 'data_value'},
        'methods': {
            'data': {'path': '/data'}
        }
    }, loop=test_api_server._loop, mode='sync')

    with client:
        data = client.data()
        assert data['data'] == 'data_value'

    assert client.data
