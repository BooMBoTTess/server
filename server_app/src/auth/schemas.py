from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: UUID
    email: str

    fk_post_id: int
    fk_department_id: int

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str

    fk_post_id: int
    fk_department_id: int

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class LoginRequest(BaseModel):
    email: str
    password: str


# class UserUpdate(schemas.BaseUserUpdate):