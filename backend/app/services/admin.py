from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users
from app.schemas import UserOut
from typing import List


class AdminService:
    async def get_items(self, db: AsyncSession) -> List[UserOut]:
        all_admins = await db.execute(select(users.Admin))
        return all_admins.scalars().all()


async def get_admin_service() -> AdminService:
    return AdminService()
