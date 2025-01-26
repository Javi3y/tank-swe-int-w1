from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users
from app.schemas import UserIn


class UserService:
    async def get_item(self, id: int, db: AsyncSession):
        admin = await db.execute(
            select(users.Admin).where(users.Admin.id == id)
        )
        return admin.scalar()
