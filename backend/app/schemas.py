from __future__ import annotations
from typing import List, Union
from pydantic import (
    BaseModel,
    EmailStr,
)
from typing import Union
import datetime

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


class UserIn(UserBase):
    password: int


class UserOut(UserBase):
    id: int


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
    name: Union[str, None] = None
    sur_name: Union[str, None] = None
    phone_number: Union[str, None] = None


class City(BaseModel):
    name: str


class AuthorBase(ClientBase):
    city: City
    goodreads: str


class AuthorOut(AuthorBase):
    id: int


class Book(BaseModel):
    title: str
    isbn: str
    price: int
    units: int
    description: str


class BookOut(Book):
    id: int
    authors: List[AuthorOut]


class BookAuthor(BaseModel):
    id: int
    author_id: int
    book_id: int


class Auth(BaseModel):
    username: str
    password: str


class ReservationIn(BaseModel):
    book_id: int

class ReservationOut(BaseModel):
    id: int
    book: BookOut
    created_at: datetime.datetime
