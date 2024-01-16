from typing import Optional

from pydantic.generics import GenericModel


class RequestBase(GenericModel):
    user: int | None = None
    sessionUser: int | None = None
    count: int | None = None
    index: Optional[int]
    size: Optional[int]
