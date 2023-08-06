from asynciorm.base.manager import BaseManager


class PostgresManager(BaseManager):

    async def fetchone(self):
        return await self._connector.fetchrow(self.query)

    async def fetchall(self):
        return await self._connector.fetch(self.query)

    async def execute(self):
        await self._connector.execute(self.query)

    async def fetch_row(self):
        return await self._connector.fetch(self.query)
