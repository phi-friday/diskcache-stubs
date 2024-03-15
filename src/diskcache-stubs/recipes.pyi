from .core import ENOVAL as ENOVAL, args_to_key as args_to_key, full_name as full_name
from _typeshed import Incomplete

class Averager:
    def __init__(
        self,
        cache,
        key,
        expire: Incomplete | None = None,
        tag: Incomplete | None = None,
    ) -> None: ...
    def add(self, value) -> None: ...
    def get(self): ...
    def pop(self): ...

class Lock:
    def __init__(
        self,
        cache,
        key,
        expire: Incomplete | None = None,
        tag: Incomplete | None = None,
    ) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def locked(self): ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info) -> None: ...

class RLock:
    def __init__(
        self,
        cache,
        key,
        expire: Incomplete | None = None,
        tag: Incomplete | None = None,
    ) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info) -> None: ...

class BoundedSemaphore:
    def __init__(
        self,
        cache,
        key,
        value: int = 1,
        expire: Incomplete | None = None,
        tag: Incomplete | None = None,
    ) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info) -> None: ...

def throttle(
    cache,
    count,
    seconds,
    name: Incomplete | None = None,
    expire: Incomplete | None = None,
    tag: Incomplete | None = None,
    time_func=...,
    sleep_func=...,
): ...
def barrier(
    cache,
    lock_factory,
    name: Incomplete | None = None,
    expire: Incomplete | None = None,
    tag: Incomplete | None = None,
): ...
def memoize_stampede(
    cache,
    expire,
    name: Incomplete | None = None,
    typed: bool = False,
    tag: Incomplete | None = None,
    beta: int = 1,
    ignore=(),
): ...
