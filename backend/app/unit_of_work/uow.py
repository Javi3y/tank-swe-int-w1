from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base import BaseRepository


class UnitOfWork():
    session: AsyncSession
    repo: BaseRepository
    def __init__(self, session: AsyncSession, repo: type[BaseRepository]):
        self.session = session
        self.repo = repo(session)
        
    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.session.rollback()
