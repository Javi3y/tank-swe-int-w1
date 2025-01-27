from typing import List
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.database import get_db
from fastapi import Depends
from app.services.users import get_user_service, UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_items(db)
