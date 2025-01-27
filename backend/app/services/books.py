from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import books
from app.schemas import BookOut
from typing import List


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


async def get_book_service() -> BookService:
    return BookService()
