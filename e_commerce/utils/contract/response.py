from typing import TypeVar, Generic, List, Optional

from ..contract.response_base import ResponseBase

T = TypeVar("T")


class Response(ResponseBase, Generic[T]):
    item: Optional[T]
    items: Optional[List[T]]
