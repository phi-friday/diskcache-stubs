import sqlite3
import warnings
from typing import (
    Any,
    BinaryIO,
    Callable,
    Container,
    ContextManager,
    Final,
    Generator,
    Iterator,
    Literal,
    Protocol,
    overload,
)

from _typeshed import StrOrBytesPath
from typing_extensions import Self, TypedDict, Unpack

__all__ = [
    "DBNAME",
    "ENOVAL",
    "UNKNOWN",
    "MODE_NONE",
    "MODE_RAW",
    "MODE_BINARY",
    "MODE_TEXT",
    "MODE_PICKLE",
    "DEFAULT_SETTINGS",
    "METADATA",
    "EVICTION_POLICY",
    "Cache",
    "Disk",
    "JSONDisk",
    "args_to_key",
    "full_name",
    "Timeout",
    "UnknownFileWarning",
    "EmptyDirWarning",
]

# type only: start

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

class _Memoized[**P, T](Protocol):
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

class DefaultSettings(Settings, total=True): ...

class Metadata(TypedDict, total=False):
    count: int
    size: int
    hits: int
    misses: int

class DefaultMetadata(Metadata, total=True): ...

# type only: end

def full_name(func: Callable[..., Any]) -> str: ...

class Constant[T: str](tuple[T]):  # noqa: SLOT001
    def __new__(cls, name: T) -> Self: ...

DBNAME: Final[DbName]
ENOVAL: Final[Constant[EnovalType]]
UNKNOWN: Final[Constant[UnknownType]]
MODE_NONE: Final[ModeNone]
MODE_RAW: Final[ModeRaw]
MODE_BINARY: Final[ModeBinary]
MODE_TEXT: Final[ModeText]
MODE_PICKLE: Final[ModePickle]
DEFAULT_SETTINGS: DefaultSettings
METADATA: DefaultMetadata
EVICTION_POLICY: dict[EvictionPolicyKey, EvictionPolicyItem]

class Disk:
    min_file_size: int
    pickle_protocol: int
    def __init__(
        self,
        directory: StrOrBytesPath,
        min_file_size: int = ...,
        pickle_protocol: int = ...,
    ) -> None: ...
    @overload
    def hash(self, key: KeyType) -> int: ...
    @overload
    def hash(self, key: KeyType) -> int: ...
    @overload
    def put(self, key: bytes) -> tuple[sqlite3.Binary, Literal[True]]: ...
    @overload
    def put[T: str | int | float](self, key: T) -> tuple[T, Literal[True]]: ...
    @overload
    def put(self, key: KeyType) -> tuple[sqlite3.Binary, Literal[False]]: ...
    @overload
    def get(self, key: sqlite3.Binary, raw: Literal[True]) -> bytes: ...
    @overload
    def get[T](self, key: T, raw: Literal[True]) -> bytes | T: ...
    @overload
    def get(self, key: KeyType, raw: Literal[False]) -> Any: ...
    @overload
    def get(self, key: KeyType, raw: bool) -> Any: ...
    @overload
    def store[T: int | float](
        self, value: T, read: bool, key: KeyType = ...
    ) -> tuple[Literal[0], ModeRaw, None, T]: ...
    @overload
    def store(
        self, value: bytes, read: bool, key: KeyType = ...
    ) -> (
        tuple[Literal[0], ModeRaw, None, sqlite3.Binary]
        | tuple[int, ModeBinary, str, None]
    ): ...
    @overload
    def store(
        self, value: str, read: bool, key: KeyType = ...
    ) -> tuple[Literal[0], ModeRaw, None, str] | tuple[int, ModeText, str, None]: ...
    @overload
    def store(
        self, value: ValueType, read: Literal[True], key: KeyType = ...
    ) -> tuple[int, ModeBinary, str, None]: ...
    @overload
    def store(
        self, value: ValueType, read: bool, key: KeyType = ...
    ) -> (
        tuple[Literal[0], ModePickle, None, sqlite3.Binary]
        | tuple[int, ModePickle, str, None]
    ): ...
    @overload
    def fetch(
        self, mode: ModeRaw, filename: str, value: sqlite3.Binary, read: bool
    ) -> bytes: ...
    @overload
    def fetch[T](self, mode: ModeRaw, filename: str, value: T, read: bool) -> T: ...
    @overload
    def fetch(
        self, mode: ModeBinary, filename: str, value: ValueType, read: Literal[True]
    ) -> BinaryIO: ...
    @overload
    def fetch(
        self, mode: ModeBinary, filename: str, value: ValueType, read: Literal[False]
    ) -> BinaryIO: ...
    @overload
    def fetch(
        self, mode: ModeBinary, filename: str, value: ValueType, read: bool
    ) -> BinaryIO | bytes: ...
    @overload
    def fetch(
        self, mode: ModeText, filename: str, value: ValueType, read: bool
    ) -> str: ...
    @overload
    def fetch(
        self, mode: ModePickle, filename: str, value: ValueType, read: bool
    ) -> ValueType: ...
    @overload
    def fetch(
        self, mode: ModeLiteral, filename: str, value: ValueType, read: bool
    ) -> ValueType: ...
    def filename(
        self, key: KeyType = ..., value: ValueType = ...
    ) -> tuple[str, str]: ...
    def remove(self, file_path: StrOrBytesPath) -> None: ...

class JSONDisk(Disk):
    compress_level: int
    def __init__(
        self,
        directory: StrOrBytesPath,
        compress_level: int = ...,
        *,
        # Disk init args
        min_file_size: int = ...,
        pickle_protocol: int = ...,
    ) -> None: ...

class Timeout(Exception): ...  # noqa: N818
class UnknownFileWarning(UserWarning): ...
class EmptyDirWarning(UserWarning): ...

def args_to_key(
    base: tuple[Any, ...],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    typed: bool,
    ignore: Ignore,
) -> tuple[Any, ...]: ...

class _BaseCache(Protocol):
    ### Settings
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
    def __getitem__(self, key: KeyType) -> ValueType: ...
    def __contains__(self, key: KeyType) -> bool: ...
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

class Cache(_BaseCache):
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        timeout: int = ...,
        disk: type[Disk] = ...,
        **settings: Unpack[Settings],
    ) -> None: ...
    def read(self, key: KeyType, retry: bool = ...) -> ValueType: ...
    @overload
    def push(
        self,
        value: ValueType,
        prefix: None = ...,
        side: ServerSide = ...,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> int: ...
    @overload
    def push(
        self,
        value: ValueType,
        prefix: str = ...,
        side: ServerSide = ...,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> str: ...
    @overload
    def push(
        self,
        value: ValueType,
        prefix: str | None = ...,
        side: ServerSide = ...,
        expire: ExpireTime = ...,
        read: bool = ...,
        tag: Tag = ...,
        retry: bool = ...,
    ) -> str | int: ...
    @overload
    def pull(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> NullablePair[int]: ...
    @overload
    def pull(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], ExpireTime]: ...
    @overload
    def pull(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], Tag]: ...
    @overload
    def pull(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], ExpireTime, Tag]: ...
    @overload
    def pull(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> NullablePair[str]: ...
    @overload
    def pull(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], ExpireTime]: ...
    @overload
    def pull(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], Tag]: ...
    @overload
    def pull(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], ExpireTime, Tag]: ...
    @overload
    def pull(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[int]
        | tuple[NullablePair[int], Tag]
        | tuple[NullablePair[int], ExpireTime]
        | tuple[NullablePair[int], ExpireTime, Tag]
    ): ...
    @overload
    def pull(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[str]
        | tuple[NullablePair[str], Tag]
        | tuple[NullablePair[str], ExpireTime]
        | tuple[NullablePair[str], ExpireTime, Tag]
    ): ...
    @overload
    def pull(
        self,
        prefix: str | None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[Any]
        | tuple[NullablePair[Any], Tag]
        | tuple[NullablePair[Any], ExpireTime]
        | tuple[NullablePair[Any], ExpireTime, Tag]
    ): ...
    @overload
    def peek(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> NullablePair[int]: ...
    @overload
    def peek(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], ExpireTime]: ...
    @overload
    def peek(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], Tag]: ...
    @overload
    def peek(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[int], ExpireTime, Tag]: ...
    @overload
    def peek(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> NullablePair[str]: ...
    @overload
    def peek(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], ExpireTime]: ...
    @overload
    def peek(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], Tag]: ...
    @overload
    def peek(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[NullablePair[str], ExpireTime, Tag]: ...
    @overload
    def peek(
        self,
        prefix: None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[int]
        | tuple[NullablePair[int], Tag]
        | tuple[NullablePair[int], ExpireTime]
        | tuple[NullablePair[int], ExpireTime, Tag]
    ): ...
    @overload
    def peek(
        self,
        prefix: str = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[str]
        | tuple[NullablePair[str], Tag]
        | tuple[NullablePair[str], ExpireTime]
        | tuple[NullablePair[str], ExpireTime, Tag]
    ): ...
    @overload
    def peek(
        self,
        prefix: str | None = ...,
        default: Any = ...,
        side: ServerSide = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        NullablePair[Any]
        | tuple[NullablePair[Any], Tag]
        | tuple[NullablePair[Any], ExpireTime]
        | tuple[NullablePair[Any], ExpireTime, Tag]
    ): ...
    @overload
    def peekitem(
        self,
        last: bool = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> KeyValuePair[Any]: ...
    @overload
    def peekitem(
        self,
        last: bool = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[False] = ...,
        retry: bool = ...,
    ) -> tuple[KeyValuePair[Any], ExpireTime]: ...
    @overload
    def peekitem(
        self,
        last: bool = ...,
        expire_time: Literal[False] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[KeyValuePair[Any], Tag]: ...
    @overload
    def peekitem(
        self,
        last: bool = ...,
        expire_time: Literal[True] = ...,
        tag: Literal[True] = ...,
        retry: bool = ...,
    ) -> tuple[KeyValuePair[Any], ExpireTime, Tag]: ...
    @overload
    def peekitem(
        self,
        last: bool = ...,
        expire_time: bool = ...,
        tag: bool = ...,
        retry: bool = ...,
    ) -> (
        KeyValuePair[Any]
        | tuple[KeyValuePair[Any], Tag]
        | tuple[KeyValuePair[Any], ExpireTime]
        | tuple[KeyValuePair[Any], ExpireTime, Tag]
    ): ...
    def memoize[**P, T](  # noqa: PLR0913
        self,
        name: str | None = ...,
        typed: bool = ...,
        expire: ExpireTime = ...,
        tag: Tag = ...,
        ignore: Ignore = ...,
    ) -> Callable[[Callable[P, T]], _Memoized[P, T]]: ...
    def expire(self, now: ExpireTime = ..., retry: bool = ...) -> int: ...
    def iterkeys(self, reverse: bool = ...) -> Generator[Any, None, None]: ...
    def __getstate__(self) -> tuple[str, int, type[Disk]]: ...
    def __setstate__(self, state: tuple[str, int, type[Disk]]) -> None: ...
