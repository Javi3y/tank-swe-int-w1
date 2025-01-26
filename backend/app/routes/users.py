from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.database import get_db
from fastapi import Depends


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(models.User))
    return users.scalars().all()
