from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel

from server_app.src.auth import schemas
from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str

    fk_post_id: int
    fk_department_id: int

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserChange(BaseModel):
    action: int
    user_name: str
    post_id: int
    department_id: int
    is_active: bool


class StaffElem(BaseModel):
    id: str
    Username: str
    post_id: int
    post: str
    dep_id: int
    dep: str


class Staff(BaseModel):
    operation: int
    elem: list[StaffElem]

class Department(BaseModel):
    id: int
    department_name: str

class Post(BaseModel):
    id: int
    post_name: str
