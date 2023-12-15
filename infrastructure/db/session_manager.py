from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Protocol

from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.db.unitofwork import ABCUnitOfWork
from utils.logging import Logging


class ABCSessionManager(Protocol):
    @asynccontextmanager  # type: ignore
    async def make_session(self) -> AsyncSession:
        raise NotImplementedError

    def session(self) -> AsyncSession:
        """
        Get the current session everywhere
        """
        raise NotImplementedError


class SessionManager(ABCSessionManager):
    def __init__(self, uow: ABCUnitOfWork, logging: Logging):
        self._uow = uow
        self._ctx_session: ContextVar[AsyncSession] = ContextVar("db_session")
        self._logger = logging.get_logger(__name__)

    @asynccontextmanager
    async def make_session(self):
        async with self._uow as session:
            token = self._ctx_session.set(session)
            try:
                yield session
            finally:
                self._ctx_session.reset(token)

    def session(self) -> AsyncSession:
        return self._ctx_session.get()

    # """
    # Depends compatible
    # """
    # async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
    #     async with self._uow as session:
    #         yield session
