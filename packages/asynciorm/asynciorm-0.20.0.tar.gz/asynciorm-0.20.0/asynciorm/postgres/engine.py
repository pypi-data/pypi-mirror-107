import asyncio
import asyncpg
from asynciorm.base.engine import BaseEngine
from asynciorm.postgres.manager import PostgresManager


class PostgresEngine(BaseEngine):

    async def __init__(self, user, password, database, host, *args, **kwargs):
        self._user = user
        self._password = password
        self._database = database
        self._host = host
        self._connector = await self._create_connector()
        self.query_manager = PostgresManager(self._connector)

    async def _create_connector(self):
        return await asyncpg.connect(user=self._user, password=self._password, database=self._database, host=self._host)

    async def close_connection(self):
        await self._connector.close()
        await asyncio.sleep(0.1)

    @property
    async def is_connect(self):
        return self._connector._running
