from typing import List, Optional

from pydantic.main import BaseModel


class UserCourse(BaseModel):

    name: str
    level: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    name: str
    email: str

    courses: List[UserCourse]

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    is_superuser: bool


class LoginRequest(BaseModel):
    username: str
    password: str
