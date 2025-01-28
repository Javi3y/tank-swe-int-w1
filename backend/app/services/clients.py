from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import books, users
from app.schemas import BookOut, ClientCreate, ClientOut
from typing import List
from app.services.author import AuthorService
from app.services.books import BookService


class ClientService:
    async def get_items(self, db: AsyncSession) -> List[ClientOut]:
        all_clients = await db.execute(select(users.Client))
        return all_clients.scalars().all()

    # async def get_item(self, id: int, db: AsyncSession) -> BookOut:
    #    book_author = await db.execute(
    #        select(books.BookAuthor).where(books.Book.id == id)
    #    )
    #    book_author = book_author.scalar()
    #    if not book_author:
    #        raise HTTPException(HTTP_404_NOT_FOUND, detail="book_author not found")
    #    return book_author

    async def create_item(
        self,
        client: ClientCreate,
        db: AsyncSession,
    ):
        new_client = users.Client(**client.model_dump())
        new_client.typ = "client"
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        return new_client


async def get_client_service() -> ClientService:
    return ClientService()
