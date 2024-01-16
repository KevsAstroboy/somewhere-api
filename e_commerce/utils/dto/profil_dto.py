from typing import Any

from pydantic import BaseModel


class ProfilDto(BaseModel):
    id: int | None = None
    code: str | None = None
    libelle: str | None = None
    is_deleted: bool | None = False
    created_at: str | None = None
    updated_at: str | None = None
    created_by: int | None = None
    updated_by: int | None = None
    deleted_by: int | None = None

    @classmethod
    def from_model(cls, profil: "Profil") -> "ProfilDto":
        return cls(
            id=profil.id,
            code=profil.code,
            libelle=profil.libelle,
            is_deleted=profil.is_deleted,
            created_at=str(profil.created_at),
            updated_at=str(profil.updated_at),
            created_by=profil.created_by,
            updated_by=profil.updated_by,
            deleted_by=profil.deleted_by,
        )
