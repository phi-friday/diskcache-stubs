import warnings
from typing import Any, Container, ContextManager, Iterator, Literal, Protocol, overload

from _typeshed import Incomplete
from diskcache import Disk
from typing_extensions import ParamSpec, Self, TypeAlias, TypedDict, TypeVar

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_P = ParamSpec("_P")
_IntOrStrT = TypeVar("_IntOrStrT", bound=int | str)

DbName: TypeAlias = Literal["cache.db"]
ModeNone: TypeAlias = Literal[0]
ModeRaw: TypeAlias = Literal[1]
ModeBinary: TypeAlias = Literal[2]
ModeText: TypeAlias = Literal[3]
ModePickle: TypeAlias = Literal[4]
ModeLiteral: TypeAlias = ModeNone | ModeRaw | ModeBinary | ModeText | ModePickle
EnovalType: TypeAlias = Literal["ENOVAL"]
UnknownType: TypeAlias = Literal["UNKNOWN"]

ExpireTime: TypeAlias = float | None
Tag: TypeAlias = str | None
Ignore: TypeAlias = Container[int | str]

ServerSide: TypeAlias = Literal["back", "front"]
KeyValuePair: TypeAlias = tuple[_IntOrStrT, Any]
NullPair: TypeAlias = tuple[None, None]
NullablePair: TypeAlias = KeyValuePair[_IntOrStrT] | NullPair

EvictionPolicyKey: TypeAlias = Literal[
    "none", "least-recently-stored", "least-recently-used", "least-frequently-used"
]
EvictionPolicyItemKey: TypeAlias = Literal["init", "get", "cull"]
EvictionPolicyItem: TypeAlias = dict[EvictionPolicyItemKey, str | None]

class Memoized(Protocol[_P, _T_co]):
    def __call__(self, *args: _P.args, **kwds: _P.kwargs) -> _T_co: ...
    def __cache_key__(self, *args: _P.args, **kwds: _P.kwargs) -> tuple[Any, ...]: ...

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

class DefaultSettings(TypedDict, total=True):
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

class DefaultMetadata(TypedDict, total=True):
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
        key: Any,
        value: Any,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> Literal[True]: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def touch(self, key: Any, expire: ExpireTime = ..., retry: bool = ...) -> bool: ...
    def add(  # noqa: PLR0913
        self,
        key: Any,
        value: Any,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> bool: ...
    def incr(
        self, key: Any, delta: int = ..., default: int = ..., retry: bool = ...
    ) -> int: ...
    def decr(
        self, key: Any, delta: int = ..., default: int = ..., retry: bool = ...
    ) -> int: ...
    def get(  # noqa: PLR0913
        self,
        key: Any,
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
    def __getitem__(self, key: Any) -> Any: ...
    def __contains__(self, key: Any) -> bool: ...
    def pop(  # noqa: PLR0913
        self,
        key: Any,
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
    def __delitem__(self, key: Any, retry: bool = ...) -> Literal[True]: ...
    def delete(self, key: Any, retry: bool = ...) -> bool: ...
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
    def reset(self, key: str, value: _T, update: bool = ...) -> _T: ...
    @overload
    def reset(self, key: str, value: Any = ..., update: bool = ...) -> Any: ...
