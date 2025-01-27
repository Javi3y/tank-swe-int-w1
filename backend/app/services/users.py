from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users
from app.schemas import UserOut
from typing import Annotated, List


class UserService:
    async def get_items(self, db: AsyncSession) -> List[UserOut]:
        all_users = await db.execute(select(users.User))
        return all_users.scalars().all()


async def get_user_service() -> UserService:
    return UserService()
