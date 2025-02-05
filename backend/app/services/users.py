from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import users
from app.schemas import UserOut
from typing import List

from app.unit_of_work.uow import UnitOfWork


class UserService:
    async def get_items(self, uow) -> List[UserOut]:
        async with uow:
            repo = uow.repo
            return await repo.get_items()

    async def get_item(self, id: int, db: AsyncSession) -> UserOut:
        user = await db.execute(select(users.User).where(users.User.id == id))
        user = user.scalar()
        if not user:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="User not found")
        return user


async def get_user_service() -> UserService:
    return UserService()
