from typing import Any

from _typeshed import StrOrBytesPath
from typing_extensions import Unpack

from .core import DEFAULT_SETTINGS as DEFAULT_SETTINGS
from .core import ENOVAL as ENOVAL
from .core import Cache as Cache
from .core import Disk as Disk
from .core import KeyType, Settings, ValueType, _BaseCache
from .core import Timeout as Timeout
from .persistent import Deque as Deque
from .persistent import Index as Index

class FanoutCache(_BaseCache):
    def __init__(
        self,
        directory: StrOrBytesPath | None = ...,
        shards: int = ...,
        timeout: float = ...,
        disk: type[Disk] = ...,
        **settings: Unpack[Settings],
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def read(self, key: KeyType) -> ValueType: ...
    def expire(self, retry: bool = ...) -> int: ...
    def cache(
        self,
        name: str,
        timeout: int = ...,
        disk: type[Disk] | None = ...,
        **settings: Unpack[Settings],
    ) -> Cache: ...
    def deque(self, name: str, maxlen: int | None = ...) -> Deque[Any]: ...
    def index(self, name: str) -> Index[Any, Any]: ...
