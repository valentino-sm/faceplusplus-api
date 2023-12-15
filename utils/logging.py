import logging
from typing import Any

logging.basicConfig(format="%(levelname)s: %(name)s: %(message)s")


class Logger:
    def __init__(self, name: str, is_debug: bool = False) -> None:
        self._logger = logging.getLogger(name)

        level = logging.DEBUG if is_debug else logging.INFO
        self._logger.setLevel(level)

    def debug(self, message: Any) -> None:
        self._logger.log(logging.DEBUG, message)

    def info(self, message: Any) -> None:
        self._logger.log(logging.INFO, message)

    def warning(self, message: Any) -> None:
        self._logger.log(logging.WARNING, message)

    def error(self, message: Any) -> None:
        self._logger.log(logging.ERROR, message)


class Logging:
    def __init__(self, is_debug: bool) -> None:
        self._is_debug = is_debug

    def get_logger(self, name: str) -> Logger:
        return Logger(name, is_debug=self._is_debug)
