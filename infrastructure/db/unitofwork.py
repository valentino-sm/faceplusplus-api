import asyncio
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.db.engine import ABCDatabaseEngine


class ABCUnitOfWork(AbstractAsyncContextManager[AsyncSession]): ...


class SQLAlchemyUnitOfWork(ABCUnitOfWork):
    def __init__(self, db_engine: ABCDatabaseEngine):
        self._db_engine = db_engine
        self._session_maker = async_sessionmaker(bind=db_engine.get_engine())  # type: ignore

    async def __aenter__(self):
        self.session = self._session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        self.session.expunge_all()
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await asyncio.shield(self.session.close())
