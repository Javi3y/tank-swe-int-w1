from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.database import get_db
from fastapi import Depends
from app.models import users


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):

    all_users = await db.execute(select(users.User))
    return all_users.scalars().all()
