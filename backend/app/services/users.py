from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from app.models import users
from app.schemas import UserOut
from typing import Annotated, List


class UserService:
    async def get_items(self, db: AsyncSession) -> List[UserOut]:
        all_users = await db.execute(select(users.User))
        return all_users.scalars().all()

    async def get_item(self, id: int, db: AsyncSession) -> UserOut:
        user = await db.execute(select(users.User).where(users.User.id == id))
        user = user.scalar()
        if not user:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="User not found")
        return user


async def get_user_service() -> UserService:
    return UserService()
