from __future__ import annotations
from typing import Union
from pydantic import (
    BaseModel,
    EmailStr,
)
from typing import Union

# token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


# users


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    name: str
    sur_name: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserLogin(BaseModel):
    password: str


class UserUpdate(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None


class City(BaseModel):
    name: str


class AuthorBase(UserBase):
    city: int
    goodreads: str
    bank_acount: str


class AuthorCreate(AuthorBase):
    id: int
    password: str


class AuthorOut(AuthorBase):
    id: int


class AuthorUpdate(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
