from typing import List
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(client: schemas.UserCreate, db: Session = Depends(get_db)):
    new_client = models.Client(**client.model_dump())
    new_client.typ = "client"
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return {"client": new_client.email}


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = await db.execute(select(models.Client))
    return users.scalars().all()


@router.patch("/", response_model=schemas.UserOut)
async def update_user(
    updated_user: schemas.UserUpdate,
    current_client: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="user does not exist")

    client = current_client

    user_dict = updated_user.model_dump(exclude_none=True)

    for key, value in user_dict.items():
        setattr(client, key, value)

    await db.commit()
    await db.refresh(client)
    return client



@router.delete("/")
async def delete_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="user doesn't exist")

    await db.delete(current_user)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(current_user: int = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="user doesn't exist")
    return current_user
