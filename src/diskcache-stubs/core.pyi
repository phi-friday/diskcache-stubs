import sqlite3
from typing import Any, BinaryIO, Callable, Final, Generator, Literal, overload

from _typeshed import StrOrBytesPath
from typing_extensions import Self, Unpack

from ._typeshed import (
    BaseCache,
    DbName,
    DefaultMetadata,
    DefaultSettings,
    EnovalType,
    EvictionPolicyItem,
    EvictionPolicyKey,
    ExpireTime,
    Ignore,
    InitSettings,
    KeyType,
    KeyValuePair,
    Memoized,
    ModeBinary,
    ModeLiteral,
    ModeNone,
    ModePickle,
    ModeRaw,
    ModeText,
    NullablePair,
    ServerSide,
    Tag,
    UnknownType,
    ValueType,
)

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
DEFAULT_SETTINGS: Final[DefaultSettings]
METADATA: Final[DefaultMetadata]
EVICTION_POLICY: Final[dict[EvictionPolicyKey, EvictionPolicyItem]]

class Disk:
    min_file_size: int
    pickle_protocol: int
    def __init__(
        self,
        directory: StrOrBytesPath,
        min_file_size: int = ...,
        pickle_protocol: int = ...,
    ) -> None: ...
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

class Cache(BaseCache):
    @overload
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        timeout: int = ...,
        disk: type[Disk] = ...,
        **settings: Unpack[InitSettings],
    ) -> None: ...
    @overload
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        timeout: int = ...,
        disk: type[Disk] = ...,
        # FIXME
        # https://peps.python.org/pep-0728/
        # diskcache allow "disk_*" args
        **settings: Any,
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
    def pull(  # noqa: PLR0913
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
    """ Incomplete
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
    """
    def peek(  # noqa: PLR0913
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
    """ Incomplete
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
    """
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
    """ Incomplete
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
    """
    def memoize[**P, T](  # noqa: PLR0913
        self,
        name: str | None = ...,
        typed: bool = ...,
        expire: ExpireTime = ...,
        tag: Tag = ...,
        ignore: Ignore = ...,
    ) -> Callable[[Callable[P, T]], Memoized[P, T]]: ...
    def expire(self, now: ExpireTime = ..., retry: bool = ...) -> int: ...
    def iterkeys(self, reverse: bool = ...) -> Generator[Any, None, None]: ...
    def __getstate__(self) -> tuple[str, int, type[Disk]]: ...
    def __setstate__(self, state: tuple[str, int, type[Disk]]) -> None: ...
