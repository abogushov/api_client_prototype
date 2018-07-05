from ..client import APIClient


async def test_api_client_context_manager():
    client = APIClient({})

    async with client:
        assert client.session

    assert client.session is None


async def test_api_client(test_api_server):
    client = APIClient({
        'server': test_api_server.make_url(''),
        'headers': {'DATA': 'data_value'},
        'methods': {
            'data': {'path': '/data'}
        }
    })

    async with client:
        data = await client.data()
        assert data['data'] == 'data_value'
