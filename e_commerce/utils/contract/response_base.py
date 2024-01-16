from pydantic.generics import GenericModel
from typing import Optional

from ..status import Status


class ResponseBase(GenericModel):
    status: Status = Status()
    user: Optional[int]
    has_error: Optional[bool] = False
    count: Optional[int]
