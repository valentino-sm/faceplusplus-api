from typing import Any, Protocol, Sequence, TypeVar

T = TypeVar("T")


class BaseRepository(Protocol[T]):
    async def create_obj(self, model: type[T], **kwargs: Any) -> T:
        raise NotImplementedError

    async def get_by_id(self, model: type[T], id_: Any) -> T:
        raise NotImplementedError

    async def get_all(self, model: type[T]) -> Sequence[T]:
        raise NotImplementedError

    async def update_obj(self, model: type[T], id_: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    async def delete_obj(self, model: type[T], id_: Any) -> None:
        raise NotImplementedError
