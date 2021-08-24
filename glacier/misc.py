import asyncio
import inspect
from functools import wraps
from typing import Any


# https://github.com/pallets/click/issues/85#issuecomment-503464628
def coro(f: Any) -> Any:
    if not inspect.iscoroutinefunction(f):
        # not Coroutine
        return f

    @wraps(f)  # type: ignore
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return (
            asyncio.get_event_loop()
            .run_until_complete(f(*args, **kwargs))
        )  # type: ignore
    return wrapper
