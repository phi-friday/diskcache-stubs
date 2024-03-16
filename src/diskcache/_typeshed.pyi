import warnings
from typing import Any, Container, ContextManager, Iterator, Literal, Protocol, overload

from _typeshed import Incomplete
from diskcache import Disk
from typing_extensions import Self, TypedDict, TypeVar

type DbName = Literal["cache.db"]
type ModeNone = Literal[0]
type ModeRaw = Literal[1]
type ModeBinary = Literal[2]
type ModeText = Literal[3]
type ModePickle = Literal[4]
type ModeLiteral = ModeNone | ModeRaw | ModeBinary | ModeText | ModePickle
type EnovalType = Literal["ENOVAL"]
type UnknownType = Literal["UNKNOWN"]

type KeyType = Any
type ValueType = Any
type ExpireTime = float | None
type Tag = str | None
type Ignore = Container[int | str]

type ServerSide = Literal["back", "front"]
type KeyValuePair[T: int | str] = tuple[T, ValueType]
type NullPair = tuple[None, None]
type NullablePair[T: int | str] = KeyValuePair[T] | NullPair

type EvictionPolicyKey = Literal[
    "none", "least-recently-stored", "least-recently-used", "least-frequently-used"
]
type EvictionPolicyItemKey = Literal["init", "get", "cull"]
type EvictionPolicyItem = dict[EvictionPolicyItemKey, str | None]

class Memoized[**P, T](Protocol):
    def __call__(self, *args: P.args, **kwds: P.kwargs) -> T: ...
    def __cache_key__(self, *args: P.args, **kwds: P.kwargs) -> tuple[Any, ...]: ...

class Settings(TypedDict, total=False):
    statistics: int
    tag_index: int
    eviction_policy: str
    size_limit: int
    cull_limit: int
    sqlite_auto_vacuum: int
    sqlite_cache_size: int
    sqlite_journal_mode: str
    sqlite_mmap_size: int
    sqlite_synchronous: int
    disk_min_file_size: int
    disk_pickle_protocol: int

class DefaultSettings(Settings, total=True):
    statistics: int
    tag_index: int
    eviction_policy: str
    size_limit: int
    cull_limit: int
    sqlite_auto_vacuum: int
    sqlite_cache_size: int
    sqlite_journal_mode: str
    sqlite_mmap_size: int
    sqlite_synchronous: int
    disk_min_file_size: int
    disk_pickle_protocol: int

class Metadata(TypedDict, total=False):
    count: int
    size: int
    hits: int
    misses: int

class DefaultMetadata(Metadata, total=True):
    count: int
    size: int
    hits: int
    misses: int

class InitSettings(Settings, Metadata, total=False): ...

class BaseCache(Protocol):
    ### Settings
    @property
    def statistics(self) -> int: ...
    @property
    def tag_index(self) -> int: ...
    @property
    def eviction_policy(self) -> str: ...
    @property
    def size_limit(self) -> int: ...
    @property
    def cull_limit(self) -> int: ...
    @property
    def sqlite_auto_vacuum(self) -> int: ...
    @property
    def sqlite_cache_size(self) -> int: ...
    @property
    def sqlite_journal_mode(self) -> str: ...
    @property
    def sqlite_mmap_size(self) -> int: ...
    @property
    def sqlite_synchronous(self) -> int: ...
    @property
    def disk_min_file_size(self) -> int: ...
    @property
    def disk_pickle_protocol(self) -> int: ...
    ###
    @property
    def directory(self) -> str: ...
    @property
    def timeout(self) -> int: ...
    @property
    def disk(self) -> Disk: ...
    def transact(self, retry: bool = ...) -> ContextManager[None]: ...
    def set(  # noqa: PLR0913
        self,
        key: KeyType,
        value: ValueType,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> Literal[True]: ...
    def __setitem__(self, key: KeyType, value: ValueType) -> None: ...
    def touch(
        self, key: KeyType, expire: ExpireTime = ..., retry: bool = ...
    ) -> bool: ...
    def add(  # noqa: PLR0913
        self,
        key: KeyType,
        value: ValueType,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> bool: ...
    def incr(
        self, key: KeyType, delta: int = ..., default: int = ..., retry: bool = ...
    ) -> int: ...
    def decr(
        self, key: KeyType, delta: int = ..., default: int = ..., retry: bool = ...
    ) -> int: ...
    def get(  # noqa: PLR0913
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> Incomplete: ...
    """
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: Literal[True] = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[BinaryIO, ExpireTime, Tag]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: Literal[True] = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[BinaryIO, ExpireTime]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: Literal[True] = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[BinaryIO, Tag]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: Literal[True] = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> BinaryIO: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[Any, ExpireTime, Tag]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[Any, ExpireTime]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[Any, Tag]: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> ValueType: ...
    @overload
    def get(
        self,
        key: KeyType,
        default: Any = ...,
        read: bool = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> ValueType: ...
    """
    def __getitem__(self, key: KeyType) -> ValueType: ...
    def __contains__(self, key: KeyType) -> bool: ...
    def pop(  # noqa: PLR0913
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> Incomplete: ...
    """
    @overload
    def pop(
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[Any, ExpireTime, Tag]: ...
    @overload
    def pop(
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[Any, ExpireTime]: ...
    @overload
    def pop(
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[Any, Tag]: ...
    @overload
    def pop(
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> ValueType: ...
    @overload
    def pop(
        self,
        key: KeyType,
        default: Any = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> ValueType: ...
    """
    def __delitem__(self, key: KeyType, retry: bool = ...) -> Literal[True]: ...
    def delete(self, key: KeyType, retry: bool = ...) -> bool: ...
    def create_tag_index(self) -> None: ...
    def drop_tag_index(self) -> None: ...
    def check(
        self, fix: bool = ..., retry: bool = ...
    ) -> list[warnings.WarningMessage]: ...
    def evict(self, tag: str, retry: bool = ...) -> int: ...
    def cull(self, retry: bool = ...) -> int: ...
    def clear(self, retry: bool = ...) -> int: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __reversed__(self) -> Iterator[Any]: ...
    def stats(self, enable: bool = ..., reset: bool = ...) -> tuple[Any, Any]: ...
    def volume(self) -> int: ...
    def close(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *exception: object) -> None: ...
    def __len__(self) -> int: ...
    @overload
    def reset[T](self, key: str, value: T, update: bool = ...) -> T: ...
    @overload
    def reset(self, key: str, value: ValueType = ..., update: bool = ...) -> Any: ...

_KeyT = TypeVar("_KeyT", bound=KeyType, default=KeyType)  # noqa: PYI018
_ValueT = TypeVar("_ValueT", bound=ValueType, default=ValueType)  # noqa: PYI018
