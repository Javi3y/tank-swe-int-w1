from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users import UserRepository


class UserUnitOfWork():
    session: AsyncSession
    repo: UserRepository
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)
        
    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.session.rollback()
