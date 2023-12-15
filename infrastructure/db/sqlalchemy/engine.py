from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

from infrastructure.db.engine import ABCDatabaseEngine


class SQLAlchemyEngine(ABCDatabaseEngine):
    def __init__(self, url: str) -> None:
        self._db_engine = create_async_engine(url)

    def get_engine(self) -> AsyncEngine:
        return self._db_engine
