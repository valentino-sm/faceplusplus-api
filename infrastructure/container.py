from typing import Any

import punq  # type: ignore
from punq import Scope  # type: ignore


class Container:
    __instance = None

    def __new__(cls) -> "Container":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self._container = punq.Container()

    def register(
        self,
        service: Any,
        factory: Any = punq.empty,
        instance: Any = punq.empty,
        scope: Scope = Scope.transient,
        **kwargs: Any,
    ) -> "Container":
        self._container = self._container.register(  # type: ignore
            service, factory, instance, scope, **kwargs
        )
        return self

    def resolve_all(self, service: Any, **kwargs: Any) -> list[Any]:
        return self._container.resolve_all(service, **kwargs)  # type: ignore

    def resolve(self, service_key: Any, **kwargs: Any) -> Any:
        return self._container.resolve(service_key, **kwargs)  # type: ignore

    def instantiate(self, service_key: Any, **kwargs: Any) -> Any:
        return self._container.instantiate(service_key, **kwargs)  # type: ignore
