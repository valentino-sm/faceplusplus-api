from contextlib import AbstractAsyncContextManager
from typing import Any, Generic, TypeVar

from utils.logging import Logging

T = TypeVar("T")


class ABCLifespan(Generic[T], AbstractAsyncContextManager[T]): ...


class EmptyLifespan(ABCLifespan[None]):
    def __init__(
        self,
        logging: Logging,
    ) -> None:
        self._logger = logging.get_logger(__name__)

    async def __aenter__(self) -> None:
        self._logger.info("Starting Lifespan")

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self._logger.info("Stopping Lifespan")
