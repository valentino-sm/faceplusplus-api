from typing import Any, Sequence, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import DeclarativeBase

from infrastructure.db.abc_repository import BaseRepository
from infrastructure.db.session_manager import ABCSessionManager
from utils.logging import Logging

Model = TypeVar("Model", bound=DeclarativeBase)


class SQLAlchemyRepository(BaseRepository[Model]):
    def __init__(self, logging: Logging, session_manager: ABCSessionManager):
        self._logger = logging.get_logger(__name__)
        self._session_manager = session_manager

    async def create_obj(self, model: type[Model], **kwargs: Any) -> Model:
        session = self._session_manager.session()
        query = insert(model).values(**kwargs).returning(model)  # type: ignore
        return (await session.execute(query)).unique().scalar_one()  # type: ignore

    async def get_by_id(self, model: type[Model], id_: Any) -> Model:
        session = self._session_manager.session()
        query = select(model).where(model.id == id_)  # type: ignore
        return (await session.execute(query)).unique().scalar_one()  # type: ignore

    async def get_all(self, model: type[Model]) -> Sequence[Model]:
        session = self._session_manager.session()
        result = await session.execute(select(model))
        return result.scalars().all()

    async def update_obj(self, model: type[Model], id_: Any, **kwargs: Any) -> None:
        session = self._session_manager.session()
        query = update(model).where(model.id == id_).values(kwargs)  # type: ignore
        await session.execute(query)

    async def delete_obj(self, model: type[Model], id_: Any) -> None:
        session = self._session_manager.session()
        query = delete(model).where(model.id == id_)  # type: ignore
        await session.execute(query)
