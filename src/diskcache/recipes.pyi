from typing import Any, Callable, Protocol

from typing_extensions import override

from .core import ENOVAL as ENOVAL
from .core import ExpireTime, Ignore, KeyType, Tag, _BaseCache
from .core import args_to_key as args_to_key
from .core import full_name as full_name

__all__ = [
    "Averager",
    "Lock",
    "RLock",
    "BoundedSemaphore",
    "throttle",
    "barrier",
    "memoize_stampede",
]

class Averager:
    def __init__(
        self, cache: _BaseCache, key: KeyType, expire: ExpireTime = ..., tag: Tag = ...
    ) -> None: ...
    def add(self, value: float) -> None: ...
    def get(self) -> float | None: ...
    def pop(self) -> float | None: ...

class _Lock(Protocol):
    def acquire(self) -> Any: ...
    def release(self) -> Any: ...
    def __enter__(self) -> Any: ...
    def __exit__(self, *exc_info: object) -> Any: ...

class Lock(_Lock):
    def __init__(
        self, cache: _BaseCache, key: KeyType, expire: ExpireTime = ..., tag: Tag = ...
    ) -> None: ...
    def locked(self) -> bool: ...
    @override
    def acquire(self) -> None: ...
    @override
    def release(self) -> None: ...
    @override
    def __enter__(self) -> None: ...
    @override
    def __exit__(self, *exc_info: object) -> None: ...

class RLock(_Lock):
    def __init__(
        self, cache: _BaseCache, key: KeyType, expire: ExpireTime = ..., tag: Tag = ...
    ) -> None: ...
    @override
    def acquire(self) -> None: ...
    @override
    def release(self) -> None: ...
    @override
    def __enter__(self) -> None: ...
    @override
    def __exit__(self, *exc_info: object) -> None: ...

class BoundedSemaphore:
    def __init__(  # noqa: PLR0913
        self,
        cache: _BaseCache,
        key: KeyType,
        value: int = ...,
        expire: ExpireTime = ...,
        tag: Tag = ...,
    ) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info: object) -> None: ...

def throttle[**P, T](  # noqa: PLR0913
    cache: _BaseCache,
    count: int,
    seconds: float,
    name: str | None = ...,
    expire: ExpireTime = ...,
    tag: Tag = ...,
    time_func: Callable[[], float] = ...,
    sleep_func: Callable[[float], Any] = ...,
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...
def barrier[**P, T](
    cache: _BaseCache,
    lock_factory: Callable[[_BaseCache, KeyType, ExpireTime, Tag], _Lock],
    name: str | None = ...,
    expire: ExpireTime = ...,
    tag: Tag = ...,
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...
def memoize_stampede[**P, T](  # noqa: PLR0913
    cache: _BaseCache,
    expire: float,
    name: str | None = ...,
    typed: bool = ...,
    tag: Tag = ...,
    beta: float = ...,
    ignore: Ignore = ...,
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...