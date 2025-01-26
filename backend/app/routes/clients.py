from typing import List
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/")
async def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    new_client = models.Client(**client.model_dump())
    new_client.typ = "client"
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return {"client": new_client.email}


@router.get("/", response_model=List[schemas.ClientOut])
async def get_client(db: Session = Depends(get_db)):
    clients = await db.execute(select(models.Client))
    return clients.scalars().all()


@router.patch("/", response_model=schemas.ClientOut)
async def update_client(
    updated_client: schemas.ClientUpdate,
    current_client: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client does not exist")

    client = current_client

    client_dict = updated_client.model_dump(exclude_none=True)

    for key, value in client_dict.items():
        setattr(client, key, value)

    await db.commit()
    await db.refresh(client)
    return client


@router.delete("/")
async def delete_client(
    current_client: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")

    await db.delete(current_client)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.ClientOut)
async def get_profile(current_client: int = Depends(get_current_user)):
    if not current_client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")
    return current_client
