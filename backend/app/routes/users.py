from typing import List
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.database import get_db
from fastapi import Depends
from app.services.users import get_user_service, UserService
from app.unit_of_work.uow import UnitOfWork
from app.repository.users import UserRepository


router = APIRouter(prefix="/users", tags=["Users"])

def get_uow(repo_cls):
    async def _get_uow(db: AsyncSession = Depends(get_db)) -> UnitOfWork:
        return UnitOfWork(db, repo_cls)
    return Depends(_get_uow)

@router.get("/", response_model=List[schemas.UserOut])
async def get_users(
    user_service: UserService = Depends(get_user_service),
    uow: UnitOfWork = get_uow(UserRepository)
):
    return await user_service.get_items(uow)
