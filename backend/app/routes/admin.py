from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.sql.functions import current_user
from starlette.status import HTTP_401_UNAUTHORIZED
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session, selectinload

router = APIRouter(prefix="/admin", tags=["Admins"])


def check_admin(admin):
    print(admin.typ)
    if admin.typ != models.Typ("admin"):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="you are not an admin")

@router.get("/", response_model=List[schemas.UserOut])
async def get_admin(current_admin: int = Depends(get_current_user), db: Session = Depends(get_db)):
    check_admin(current_admin)
    admins = await db.execute(
        select(models.Admin)
    )
    return admins.scalars().all()

@router.get("/profile", response_model=schemas.AuthorOut)
async def get_profile(current_admin: int = Depends(get_current_user), db: Session = Depends(get_db)):
    author = await db.execute(
        select(models.Admin)
        .where(models.Admin.id == current_admin.id)
    )
    return author.scalar()
