import asyncio
from typing import Dict

from aiohttp import ClientSession


class APIClient:
    def __init__(self, config: Dict, loop=None, mode='async') -> None:
        self._config = config
        self._session = None
        self._loop = loop or asyncio.get_event_loop()
        self._mode = mode
        self._headers = config.get('headers')

    @property
    def session(self) -> ClientSession:
        """An internal aiohttp.ClientSession.
        """
        return self._session

    def __getattr__(self, item):
        method_config = self._config.get('methods', {}).get(item)
        if method_config:
            if self._mode == 'async':
                async def do(**kwargs):
                    r = await self.request(**method_config, **kwargs)
                    return await r.json()
                return do
            else:
                def do(**kwargs):
                    async def async_do():
                        response = await self.request(**method_config, **kwargs)
                        data = await response.json()
                        return data
                    return self._loop.run_until_complete(async_do())
                return do

    async def __aenter__(self):
        if self._session:
            return self
        self._session = ClientSession(loop=self._loop)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        if self._session:
            return self

        self._session = ClientSession(loop=self._loop)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.close()
            self._session = None

    async def request(self, path: str, **kwargs):
        url = f'{self._config["server"]}{path}'
        if self.session:
            return await self.session.get(url, headers=self._headers)
        async with ClientSession(loop=self._loop) as session:
            return await session.get(url, headers=self._headers)
