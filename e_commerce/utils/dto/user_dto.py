from pydantic import BaseModel


class UserDto(BaseModel):
    id: int | None = None
    nom: str | None = None
    prenom: str | None = None
    matricule: str | None = None
    login: str | None = None
    password: str | None = None
    contact: str | None = None
    profil_id: int | None = None
    profil_libelle: str | None = None
    is_locked: bool | None = False
    is_super_admin: bool | None = False
    is_deleted: bool | None = False
    created_at: str | None = None
    updated_at: str | None = None
    created_by: int | None = None
    updated_by: int | None = None
    deleted_by: int | None = None