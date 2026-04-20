import clickhouse_connect
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.config import settings

_client: AsyncClient | None = None


async def get_clickhouse_client() -> AsyncClient:
    global _client
    if _client is None:
        _client = await clickhouse_connect.get_async_client(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
        )
    return _client


async def get_db() -> AsyncClient:
    client = await get_clickhouse_client()
    yield client
