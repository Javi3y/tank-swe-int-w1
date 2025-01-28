from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from app.models import books
from app.schemas import Book, BookOut
from typing import List

from app.services.author import AuthorService
from app.services.users import UserService


class BookService:
    async def get_items(self, db: AsyncSession) -> List[BookOut]:
        all_books = await db.execute(select(books.Book))
        return all_books.scalars().all()

    async def get_item(self, id: int, db: AsyncSession) -> BookOut:
        book = await db.execute(select(books.Book).where(books.Book.id == id))
        book = book.scalar()
        if not book:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="book not found")
        return book

    async def get_authors(self, id: int, db: AsyncSession):
        book = await self.get_item(id, db)
        return book.authors

    async def create_item(
        self,
        book: Book,
        user: int,
        author_service: AuthorService,
        book_author_service: "BookAuthorService",
        book_service: "BookService",
        db: AsyncSession,
        id: int | None = None,
    ):
        if id:
            if user.typ.value != "admin":
                raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Must be admin")
            author_id = id
        else:
            author_id = user.id

        new_book = books.Book(**book.model_dump())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        await book_author_service.create_item(
            author_id, new_book.id, book_service, author_service, db
        )
        return {"book": new_book.title}

    async def delete_item(self, user, id: int, db: AsyncSession):
        if user.typ.value != "admin":
            raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Must be admin")
        book = await self.get_item(id, db)
        await db.delete(book)
        await db.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)


async def get_book_service() -> BookService:
    return BookService()
