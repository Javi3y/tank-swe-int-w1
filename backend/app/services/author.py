from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import users
from app.schemas import AuthorOut
from typing import List


class AuthorService:
    async def get_items(self, db: AsyncSession) -> List[AuthorOut]:
        all_authors = await db.execute(select(users.Author))
        return all_authors.scalars().all()

    async def get_item(self, id: int, db: AsyncSession):
        author = await db.execute(select(users.Author).where(users.Author.id == id))
        author = author.scalar()
        if not author:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="author does not exist")
        print(author)
        return author


async def get_author_service() -> AuthorService:
    return AuthorService()
