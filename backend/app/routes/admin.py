from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED
from app import schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from app.models import users
from app.services.admin import AdminService, get_admin_service

router = APIRouter(prefix="/admin", tags=["Admins"])


async def check_admin(admin):
    if admin.typ != users.Typ("admin"):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="you are not an admin")


@router.get("/", response_model=List[schemas.UserOut])
async def get_admin(
    current_admin: users.Admin = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    admin_service: AdminService = Depends(get_admin_service),
):
    await check_admin(current_admin)
    return await admin_service.get_items(db)


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(
    current_admin: users.Admin = Depends(get_current_user),
):
    await check_admin(current_admin)
    return current_admin
