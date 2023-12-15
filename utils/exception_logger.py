import functools
import inspect
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar

from utils.exceptions import LoudError, QuietError
from utils.logging import Logging

T = TypeVar("T")
P = ParamSpec("P")
_A = Awaitable
_C = Callable
_G = Coroutine


class ExceptionLogger:
    def __init__(self, logging: Logging) -> None:
        self._logger = logging.get_logger(__name__)

    def _get_exception_str(self, e: BaseException) -> str:
        frm = inspect.trace()[-1]
        module = inspect.getmodule(frm[0])
        module_name = module.__name__ if module else "UnknownModule"
        return f"{module_name}: {type(e).__name__}: {e}"

    def wrap(self, func: _C[P, _A[T]]) -> _C[P, _G[Any, Any, T | None]]:
        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            try:
                return await func(*args, **kwargs)
            except QuietError as e:
                line = self._get_exception_str(e)
                self._logger.warning(line)
            except LoudError as e:
                line = self._get_exception_str(e)
                self._logger.error(line)
            except Exception as e:
                line = self._get_exception_str(e)
                self._logger.error(line)
                raise e

        return async_wrapper
