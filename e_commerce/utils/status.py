from pydantic import BaseModel


class Status(BaseModel):
    code: int | None = 800
    message: str | None = "Operation effectuée avec succès."
