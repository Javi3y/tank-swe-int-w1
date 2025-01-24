from enum import Enum
from typing import Optional, Union
from pydantic import (
    UUID4,
    BaseModel,
    EmailStr,
)

# token

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


# users


class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(User):
    password: str


class UserOut(User):
    id: int


class UserLogin(User):
    password: str


class UserUpdate(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
