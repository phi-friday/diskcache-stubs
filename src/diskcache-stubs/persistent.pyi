from collections.abc import MutableMapping, Sequence
from typing import (
    Any,
    Callable,
    ContextManager,
    Generic,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    ValuesView,
    overload,
)

from _typeshed import StrOrBytesPath
from diskcache.core import Cache
from typing_extensions import ParamSpec, Self, TypeVar

from ._typeshed import (
    Ignore,
    KeyValuePair,
    Memoized,
    NullablePair,
    ServerSide,
    ValueType,
    _KeyT,
    _ValueT,
)

__all__ = ["Deque", "Index"]

_T = TypeVar("_T", infer_variance=True)
_P = ParamSpec("_P")
_AnyDefault: Iterable[Any] = ()
_AnyT = TypeVar("_AnyT", bound=Any, infer_variance=True)
_ValueWithoutDefaultT = TypeVar(
    "_ValueWithoutDefaultT", bound=ValueType, infer_variance=True
)

class Deque(Sequence[_ValueT], Generic[_ValueT]):
    __hash__: None
    def __init__(
        self,
        iterable: Iterable[_ValueT] = _AnyDefault,  # noqa: PYI011
        directory: StrOrBytesPath | None = ...,
        maxlen: int | None = ...,
    ) -> None: ...
    @overload
    @classmethod
    def fromcache(
        cls, cache: Cache, iterable: Iterable[_AnyT], maxlen: int | None = ...
    ) -> Deque[_AnyT]: ...
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
    def __iadd__(self, iterable: Iterable[_ValueT]) -> Self: ...
    def __iter__(self) -> Iterator[ValueType]: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Iterator[ValueType]: ...
    def __getstate__(self) -> tuple[str, int]: ...
    def __setstate__(self, state: tuple[str, int]) -> None: ...
    def append(self, value: _ValueT) -> None: ...
    def appendleft(self, value: _ValueT) -> None: ...
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    def count(self, value: _ValueT) -> int: ...
    def extend(self, iterable: Iterable[_ValueT]) -> None: ...
    def extendleft(self, iterable: Iterable[_ValueT]) -> None: ...
    def peek(self) -> _ValueT: ...
    def peekleft(self) -> _ValueT: ...
    def pop(self) -> _ValueT: ...
    def popleft(self) -> _ValueT: ...
    def remove(self, value: _ValueT) -> _ValueT: ...
    def reverse(self) -> None: ...
    def rotate(self, steps: int = ...) -> None: ...
    def transact(self) -> ContextManager[None]: ...

class Index(MutableMapping[_KeyT, _ValueT], Generic[_KeyT, _ValueT]):
    __hash__: None
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def fromcache(
        cls, cache: Cache, *args: Any, **kwargs: _ValueWithoutDefaultT
    ) -> Index[str, _ValueWithoutDefaultT]: ...
    @property
    def cache(self) -> Cache: ...
    @property
    def directory(self) -> str: ...
    def __getitem__(self, key: _KeyT) -> _ValueT: ...
    def __setitem__(self, key: _KeyT, value: _ValueT) -> None: ...
    def __delitem__(self, key: _KeyT) -> None: ...
    @overload
    def setdefault(self, key: _KeyT, default: _ValueT | None = ...) -> _ValueT: ...
    @overload
    def setdefault(self, key: _KeyT, default: Any = ...) -> Any: ...
    def peekitem(self, last: bool = ...) -> KeyValuePair[Any]: ...
    @overload
    def pop(self, key: _KeyT, default: _ValueT = ...) -> _ValueT: ...
    @overload
    def pop(self, key: _KeyT, default: Any = ...) -> Any: ...
    def popitem(self, last: bool = True) -> KeyValuePair[Any]: ...
    @overload
    def push(
        self, value: _ValueT, prefix: None = ..., side: ServerSide = ...
    ) -> int: ...
    @overload
    def push(
        self, value: _ValueT, prefix: str = ..., side: ServerSide = ...
    ) -> str: ...
    @overload
    def push(
        self, value: _ValueT, prefix: str | None = ..., side: ServerSide = ...
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
    def keys(self) -> KeysView[_KeyT]: ...
    def values(self) -> ValuesView[_ValueT]: ...
    def items(self) -> ItemsView[_KeyT, _ValueT]: ...
    def __getstate__(self) -> str: ...
    def __setstate__(self, state: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def memoize(
        self, name: str | None = ..., typed: bool = ..., ignore: Ignore = ...
    ) -> Callable[[Callable[_P, _T]], Memoized[_P, _T]]: ...
    def transact(self) -> ContextManager[None]: ...
