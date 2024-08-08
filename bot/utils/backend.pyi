from typing import Any
from ..enums.operation_type import OperationType

# TODO: use aiohttp

class APIHandler:
    host: str = ...
    port: str = ...

    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc, tb): ...
    async def crud(
        self,
        entity_name: str,
        operation_type: str | OperationType = ...,  # READ by default
        data: dict[str:Any] = ...,  # None by default
    ): ...
