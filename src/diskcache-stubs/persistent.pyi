from .core import Cache as Cache, ENOVAL as ENOVAL
from _typeshed import Incomplete
from collections.abc import Generator, MutableMapping, Sequence

class Deque(Sequence):
    def __init__(
        self,
        iterable=(),
        directory: Incomplete | None = None,
        maxlen: Incomplete | None = None,
    ) -> None: ...
    @classmethod
    def fromcache(cls, cache, iterable=(), maxlen: Incomplete | None = None): ...
    @property
    def cache(self): ...
    @property
    def directory(self): ...
    @property
    def maxlen(self): ...
    @maxlen.setter
    def maxlen(self, value) -> None: ...
    def __getitem__(self, index): ...
    def __setitem__(self, index, value) -> None: ...
    def __delitem__(self, index) -> None: ...
    __eq__: Incomplete
    __ne__: Incomplete
    __lt__: Incomplete
    __gt__: Incomplete
    __le__: Incomplete
    __ge__: Incomplete
    def __iadd__(self, iterable): ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Generator[Incomplete, None, None]: ...
    def append(self, value) -> None: ...
    def appendleft(self, value) -> None: ...
    def clear(self) -> None: ...
    def copy(self): ...
    def count(self, value): ...
    def extend(self, iterable) -> None: ...
    def extendleft(self, iterable) -> None: ...
    def peek(self): ...
    def peekleft(self): ...
    def pop(self): ...
    def popleft(self): ...
    def remove(self, value) -> None: ...
    def reverse(self) -> None: ...
    def rotate(self, steps: int = 1) -> None: ...
    __hash__: Incomplete
    def transact(self) -> Generator[None, None, None]: ...

class Index(MutableMapping):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def fromcache(cls, cache, *args, **kwargs): ...
    @property
    def cache(self): ...
    @property
    def directory(self): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    def __delitem__(self, key) -> None: ...
    def setdefault(self, key, default: Incomplete | None = None): ...
    def peekitem(self, last: bool = True): ...
    def pop(self, key, default=...): ...
    def popitem(self, last: bool = True): ...
    def push(self, value, prefix: Incomplete | None = None, side: str = "back"): ...
    def pull(
        self,
        prefix: Incomplete | None = None,
        default=(None, None),
        side: str = "front",
    ): ...
    def clear(self) -> None: ...
    def __iter__(self): ...
    def __reversed__(self): ...
    def __len__(self) -> int: ...
    def keys(self): ...
    def values(self): ...
    def items(self): ...
    __hash__: Incomplete
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def memoize(
        self, name: Incomplete | None = None, typed: bool = False, ignore=()
    ): ...
    def transact(self) -> Generator[None, None, None]: ...
