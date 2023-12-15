"""
    FastAPI Builder
"""

from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

from fastapi import FastAPI as _FastAPI

from infrastructure.lifespan import ABCLifespan
from presentation.asgi.abc_builder import ASGIApp, ASGIAppBuilder
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from presentation.asgi.fastapi.exception_handler import (exception_handler,
                                                         responses)
from utils.logging import Logging


class FastAPIAppBuilder(ASGIAppBuilder):
    def __init__(
        self,
        logging: Logging,
        router_builders: list[ABCRouterBuilder],
        lifespans: list[ABCLifespan],  # type: ignore - hack for DI Container
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._router_builders = router_builders
        self._lifespans: list[ABCLifespan[Any]] = lifespans

    def create_app(self) -> ASGIApp:
        self._app = _FastAPI(lifespan=self._lifespan_for_every_worker)
        self._app.router.responses.update(responses)  # type: ignore

        for router_builder in self._router_builders:
            self._logger.debug(
                f"Registering router from {router_builder.__class__.__name__}"
            )
            router = router_builder.create_router()
            self._app.include_router(router)

        @self._app.exception_handler(Exception)
        async def _(request: Any, exception: Exception) -> Any:
            return await exception_handler(request, exception)

        return self._app

    @asynccontextmanager
    async def _lifespan_for_every_worker(self, _: ASGIApp):
        async with AsyncExitStack() as stack:
            for lifespan in self._lifespans:
                await stack.enter_async_context(lifespan)
            yield
