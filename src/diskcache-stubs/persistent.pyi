from collections.abc import MutableMapping, Sequence
from typing import (
    Any,
    ContextManager,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    ValuesView,
    overload,
)

from _typeshed import StrOrBytesPath
from typing_extensions import Self

from .core import ENOVAL as ENOVAL
from .core import Cache as Cache
from .core import (
    Ignore,
    KeyType,
    KeyValuePair,
    NullablePair,
    ServerSide,
    ValueType,
    _Memoized,
)

class Deque[T: Any](Sequence[T]):
    __hash__: None
    def __init__(
        self,
        iterable: Iterable[T] = (),
        directory: StrOrBytesPath | None = ...,
        maxlen: int | None = ...,
    ) -> None: ...
    @overload
    @classmethod
    def fromcache[T2: Any](
        cls, cache: Cache, iterable: Iterable[T2], maxlen: int | None = ...
    ) -> Deque[T2]: ...
    @overload
    @classmethod
    def fromcache(
        cls, cache: Cache, iterable: Iterable[Any] = ..., maxlen: int | None = ...
    ) -> Deque[Any]: ...
    @property
    def cache(self) -> Cache: ...
    @property
    def directory(self) -> str: ...
    @property
    def maxlen(self) -> int: ...
    @maxlen.setter
    def maxlen(self, value: int) -> None: ...
    def __getitem__(self, index: int) -> ValueType: ...
    def __setitem__(self, index: int, value: ValueType) -> None: ...
    def __delitem__(self, index: int) -> None: ...
    def __eq__(self, value: object) -> bool: ...
    def __ne__(self, value: object) -> bool: ...
    def __lt__(self, value: object) -> bool: ...
    def __gt__(self, value: object) -> bool: ...
    def __le__(self, value: object) -> bool: ...
    def __ge__(self, value: object) -> bool: ...
    def __iadd__(self, iterable: Iterable[T]) -> Self: ...
    def __iter__(self) -> Iterator[ValueType]: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Iterator[ValueType]: ...
    def __getstate__(self) -> tuple[str, int]: ...
    def __setstate__(self, state: tuple[str, int]) -> None: ...
    def append(self, value: T) -> None: ...
    def appendleft(self, value: T) -> None: ...
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    def count(self, value: T) -> int: ...
    def extend(self, iterable: Iterable[T]) -> None: ...
    def extendleft(self, iterable: Iterable[T]) -> None: ...
    def peek(self) -> T: ...
    def peekleft(self) -> T: ...
    def pop(self) -> T: ...
    def popleft(self) -> T: ...
    def remove(self, value: T) -> T: ...
    def reverse(self) -> None: ...
    def rotate(self, steps: int = ...) -> None: ...
    def transact(self) -> ContextManager[None]: ...

class Index[K: KeyType, V: ValueType](MutableMapping[K, V]):
    __hash__: None
    def __init__(self, *args: Any, **kwargs: V) -> None: ...
    @classmethod
    def fromcache[V2: ValueType](
        cls, cache: Cache, *args: Any, **kwargs: V2
    ) -> Index[str, V2]: ...
    @property
    def cache(self) -> Cache: ...
    @property
    def directory(self) -> str: ...
    def __getitem__(self, key: K) -> V: ...
    def __setitem__(self, key: K, value: V) -> None: ...
    def __delitem__(self, key: K) -> None: ...
    @overload
    def setdefault(self, key: K, default: V | None = ...) -> V: ...
    @overload
    def setdefault(self, key: K, default: Any = ...) -> Any: ...
    def peekitem(self, last: bool = ...) -> KeyValuePair[Any]: ...
    @overload
    def pop(self, key: K, default: V = ...) -> V: ...
    @overload
    def pop(self, key: K, default: Any = ...) -> Any: ...
    def popitem(self, last: bool = True) -> KeyValuePair[Any]: ...
    @overload
    def push(self, value: V, prefix: None = ..., side: ServerSide = ...) -> int: ...
    @overload
    def push(self, value: V, prefix: str = ..., side: ServerSide = ...) -> str: ...
    @overload
    def push(
        self, value: V, prefix: str | None = ..., side: ServerSide = ...
    ) -> str | int: ...
    @overload
    def pull(
        self, prefix: None = ..., default: Any = ..., side: ServerSide = ...
    ) -> NullablePair[int]: ...
    @overload
    def pull(
        self, prefix: str = ..., default: Any = ..., side: ServerSide = ...
    ) -> NullablePair[str]: ...
    @overload
    def pull(
        self, prefix: str | None = ..., default: Any = ..., side: ServerSide = ...
    ) -> NullablePair[Any]: ...
    def clear(self) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __reversed__(self) -> Iterator[Any]: ...
    def __len__(self) -> int: ...
    def keys(self) -> KeysView[K]: ...
    def values(self) -> ValuesView[V]: ...
    def items(self) -> ItemsView[K, V]: ...
    def __getstate__(self) -> str: ...
    def __setstate__(self, state: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def memoize[**P, T](
        self, name: str | None = ..., typed: bool = ..., ignore: Ignore = ...
    ) -> _Memoized[P, T]: ...
    def transact(self) -> ContextManager[None]: ...