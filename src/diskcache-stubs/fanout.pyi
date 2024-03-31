from typing import Any, overload

from _typeshed import StrOrBytesPath
from diskcache.core import DEFAULT_SETTINGS as DEFAULT_SETTINGS
from diskcache.core import ENOVAL as ENOVAL
from diskcache.core import Cache as Cache
from diskcache.core import Disk as Disk
from diskcache.core import Timeout as Timeout
from diskcache.persistent import Deque as Deque
from diskcache.persistent import Index as Index
from typing_extensions import Unpack

from ._typeshed import BaseCache, InitSettings, KeyType, ValueType

__all__ = ["FanoutCache"]

class FanoutCache(BaseCache):
    @overload
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        shards: int = ...,
        timeout: float = ...,
        disk: type[Disk] = ...,
        **settings: Unpack[InitSettings],
    ) -> None: ...
    @overload
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        shards: int = ...,
        timeout: float = ...,
        disk: type[Disk] = ...,
        # FIXME
        # https://peps.python.org/pep-0728/
        # diskcache allow "disk_*" args
        **settings: Any,
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def read(self, key: KeyType) -> ValueType: ...
    def expire(self, retry: bool = ...) -> int: ...
    @overload
    def cache(
        self,
        name: str,
        timeout: int = ...,
        disk: type[Disk] | None = ...,
        **settings: Unpack[InitSettings],
    ) -> Cache: ...
    @overload
    def cache(
        self,
        name: str,
        timeout: int = ...,
        disk: type[Disk] | None = ...,
        # FIXME
        # https://peps.python.org/pep-0728/
        # diskcache allow "disk_*" args
        **settings: Any,
    ) -> Cache: ...
    def deque(self, name: str, maxlen: int | None = ...) -> Deque[Any]: ...
    def index(self, name: str) -> Index[Any, Any]: ...
