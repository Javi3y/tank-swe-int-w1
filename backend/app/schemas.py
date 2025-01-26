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
    name: str
    sur_name: str

    class Config:
        from_attributes = True


class ClientBase(UserBase):
    pass


class ClientCreate(ClientBase):
    password: str
    phone_number: str


class ClientOut(ClientBase):
    id: int
    balance: int


class ClientLogin(BaseModel):
    password: str


class ClientUpdate(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None


class City(BaseModel):
    name: str


class AuthorBase(ClientBase):
    city: City
    goodreads: str


class AuthorOut(AuthorBase):
    id: int
