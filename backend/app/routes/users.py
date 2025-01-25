from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_client = models.Client(**user.model_dump())
    new_client.typ = "client"
    new_client.subscription_model = "free"
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return {"user": new_client.email}


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = await db.execute(select(models.User))
    return users.scalars().all()


@router.patch("/", response_model=schemas.UserOut)
async def update_user(
    updated_user: schemas.UserUpdate,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = current_user

    user_dict = updated_user.model_dump(exclude_none=True)

    for key, value in user_dict.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/")
async def delete_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    await db.delete(current_user)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(current_user: int = Depends(get_current_user)):
    print(current_user.phone_number)
    return current_user
