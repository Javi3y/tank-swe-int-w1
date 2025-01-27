from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import books, users
from app.schemas import BookOut
from typing import List
from app.services.author import AuthorService, get_author_service
from app.services.books import BookService, get_book_service


class BookAuthorService:
    async def get_items(self, db: AsyncSession) -> List[BookOut]:
        all_book_authors = await db.execute(select(books.BookAuthor))
        return all_book_authors.scalars().all()

    async def get_item(self, id: int, db: AsyncSession) -> BookOut:
        book_author = await db.execute(
            select(books.BookAuthor).where(books.Book.id == id)
        )
        book_author = book_author.scalar()
        if not book_author:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="book_author not found")
        return book_author

    async def create_item(
        self,
        author_id: int,
        book_id: int,
        book_service: BookService,
        author_service: AuthorService,
        db: AsyncSession,
    ):
        author = await author_service.get_item(author_id, db)
        book = await book_service.get_item(book_id, db)

        new_book_author = books.BookAuthor(author_id=author.id, book_id=book.id)
        db.add(new_book_author)
        await db.commit()

        await db.refresh(new_book_author)
        await db.refresh(author)
        await db.refresh(book)

        return new_book_author


async def get_book_author_service() -> BookAuthorService:
    return BookAuthorService()
