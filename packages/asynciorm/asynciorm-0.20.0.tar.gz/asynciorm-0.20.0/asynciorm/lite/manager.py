from asynciorm.base.manager import BaseManager


class SQLiteManager(BaseManager):

    async def fetchone(self):
        cursor = await self._connector.execute(self.query)
        return await cursor.fetchone()

    async def fetchall(self):
        cursor = await self._connector.execute(self.query)
        return await cursor.fetchall()

    async def execute(self):
        await self._connector.execute(self.query)
        await self._connector.commit()

    async def fetch_row(self):
        cursor = await self._connector.execute(self.query)
        return await cursor.fetchall()