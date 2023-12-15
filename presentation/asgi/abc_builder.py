from typing import Any, Awaitable, Callable, Protocol

ASGIApp = Callable[[Any, Any, Any], Awaitable[None]]


class ASGIAppBuilder(Protocol):
    def create_app(self) -> ASGIApp:
        raise NotImplementedError
