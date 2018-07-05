import pytest


@pytest.fixture
def test_api():
    from aiohttp import web

    async def handle(request):
        data = {'data': request.headers.get('DATA')}
        return web.json_response(data)

    app = web.Application()
    app.router.add_get('/data', handle)
    return app


@pytest.fixture
def test_api_server(loop, test_api):

    from aiohttp.test_utils import TestServer

    servers = []

    async def go():
        server = TestServer(test_api)
        await server.start_server(loop=loop)
        servers.append(server)
        return server

    server = loop.run_until_complete(go())

    yield server

    async def finalize():
        while servers:
            await servers.pop().close()

    loop.run_until_complete(finalize())
