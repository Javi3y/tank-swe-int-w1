from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users
from app.schemas import UserIn


class UserService:
    async def create_item(self, user:UserIn, db: AsyncSession):
        new_user = users.User(**user.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
