from typing import Any, Protocol

from httpx import AsyncClient
from tenacity import (retry, retry_if_exception_type,
                      retry_if_result, stop_after_attempt, wait_exponential,
                      wait_random)

from utils.logging import Logging


class ABCHTTPClient(Protocol):
    async def request(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError

    async def get(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError

    async def post(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError


class HTTPXUtils:
    @staticmethod
    def is_not_valid(value: Any) -> bool:
        return not isinstance(value, dict) or not value


class HTTPXClient(ABCHTTPClient):
    def __init__(self, logging: Logging) -> None:
        self._logger = logging.get_logger(__name__)

    @retry(
        retry=retry_if_result(HTTPXUtils.is_not_valid)
        | retry_if_exception_type(Exception),
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=10)
        + wait_random(min=0.1, max=0.5),
    )
    async def request(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        async with AsyncClient() as client:
            response = await client.request(*args, **kwargs)
        self._logger.debug(f"Status: {response.status_code}")
        # response.raise_for_status()
        return response.json()

    async def get(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return await self.request("GET", *args, **kwargs)

    async def post(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return await self.request("POST", *args, **kwargs)
