from typing import List
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from app import schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from app.models import users, books
from app.services.author import AuthorService, get_author_service
from app.services.bookauthor import BookAuthorService, get_book_author_service
from app.services.books import BookService, get_book_service


router = APIRouter(prefix="/books", tags=["Books"])


async def check_admin(user):
    if user.typ != users.Typ("admin") and user.typ != users.Typ("author"):
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="user doesn't have the permisions for this operation",
        )


@router.post("/")
async def create_book(
    book: schemas.Book,
    current_user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await check_admin(current_user)
    new_book = books.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return {"book": new_book.title}


@router.get("/", response_model=List[schemas.BookOut])
async def get_books(
    book_service: BookService = Depends(get_book_service),
    db: AsyncSession = Depends(get_db),
):
    return await book_service.get_items(db)


#
#
# @router.patch("/", response_model=schemas.ClientOut)
# async def update_client(
#    updated_client: schemas.ClientUpdate,
#    current_client: int = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
# ):
#    if not client:
#        raise HTTPException(HTTP_404_NOT_FOUND, detail="client does not exist")
#
#    client = current_client
#
#    client_dict = updated_client.model_dump(exclude_none=True)
#
#    for key, value in client_dict.items():
#        setattr(client, key, value)
#
#    await db.commit()
#    await db.refresh(client)
#    return client
#
#
# @router.delete("/")
# async def delete_client(
#    current_client: users.User = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
# ):
#    if not current_client:
#        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")
#
#    await db.delete(current_client)
#    await db.commit()
#    return Response(status_code=HTTP_204_NO_CONTENT)
#
#
@router.get("/{id}", response_model=schemas.BookOut)
async def get_book(
    id: int,
    book_service: BookService = Depends(get_book_service),
    db: AsyncSession = Depends(get_db),
):
    return await book_service.get_item(id, db)


@router.get("/{id}/authors", response_model=List[schemas.AuthorOut])
async def get_authors(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    book = await db.execute(select(books.Book).where(books.Book.id == id))
    book = book.scalar()
    if not book:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="book not found")

    return book.authors


@router.post("/{id}/authors", response_model=schemas.BookAuthor)
async def add_author(
    id: int,
    author: int,
    current_user: int = Depends(get_current_user),
    author_service: AuthorService = Depends(get_author_service),
    book_service: BookService = Depends(get_book_service),
    book_author_service: BookAuthorService = Depends(get_book_author_service),
    db: AsyncSession = Depends(get_db),
):
    return await book_author_service.create_item(
        author, id, book_service, author_service, db
    )


@router.delete("/{id}/{author_id}")
async def delete_author(
    id: int,
    author_id: int,
    current_user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await check_admin(current_user)

    book = await db.execute(select(books.Book).where(books.Book.id == id))
    book = book.scalar()
    if not book:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="book not found")
    author = await db.execute(select(users.Author).where(users.Author.id == author_id))
    author = author.scalar()
    if not author:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="author not found")
    author_book = await db.execute(
        select(books.BookAuthor)
        .where(books.BookAuthor.book_id == book.id)
        .where(books.BookAuthor.author_id == author.id)
    )
    author_book = author_book.scalar()
    await db.delete(author_book)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
