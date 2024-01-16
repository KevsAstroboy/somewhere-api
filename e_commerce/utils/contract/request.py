from typing import TypeVar, Generic, List, Optional

from ..contract.request_base import RequestBase

T = TypeVar("T")


class Request(RequestBase, Generic[T]):
    data: Optional[T]
    datas: Optional[List[T]]
