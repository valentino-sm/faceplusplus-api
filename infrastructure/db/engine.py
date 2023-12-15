from typing import Protocol


class ABCDatabaseEngine(Protocol):
    def __init__(self, url: str) -> None:
        raise NotImplementedError

    def get_engine(self) -> object:
        raise NotImplementedError
