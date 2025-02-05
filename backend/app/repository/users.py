from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import users

class UserRepository():
    session: AsyncSession
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        all_users = await self.session.execute(select(users.User))
        return all_users.scalars().all()


#    def flush()
#    def commit():
#        session.commit()
#    def __aexit__:
#        self.rollback()
#    with uow() as uow:
#    
#        REPO = rEPO(uow.session)
#        repo = uow.folan_repo
#        ewpo.add
#        uow.persist
#
#
#
#
#
#
#        comitt

