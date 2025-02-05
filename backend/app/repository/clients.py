from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users
from app.repository.base import BaseRepository

class ClientRepository(BaseRepository):
    session: AsyncSession
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_items(self):
        all_clients = await self.session.execute(select(users.Client))
        return all_clients.scalars().all()
