from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from app import models, schemas
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.ClientOut])
async def get_users(db: Session = Depends(get_db)):
    clients = await db.execute(select(models.Client))
    return clients.scalars().all()
