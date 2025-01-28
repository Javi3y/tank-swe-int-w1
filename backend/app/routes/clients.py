from typing import List
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from app import schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from app.models import users
from app.services.clients import ClientService, get_client_service


router = APIRouter(prefix="/clients", tags=["Clients"])


# Done
@router.post("/", response_model=schemas.ClientOut)
async def create_client(
    client: schemas.ClientCreate,
    db: AsyncSession = Depends(get_db),
    client_service: ClientService = Depends(get_client_service),
):
    return await client_service.create_item(client, db)

# Done
@router.get("/", response_model=List[schemas.ClientOut])
async def get_client(
    client_service: ClientService = Depends(get_client_service),
    db: AsyncSession = Depends(get_db),
):
    return await client_service.get_items(db)


@router.patch("/", response_model=schemas.ClientOut)
async def update_client(
    updated_client: schemas.ClientUpdate,
    current_client: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_client:
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
    current_client: users.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")

    await db.delete(current_client)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.ClientOut)
async def get_profile(current_client: int = Depends(get_current_user)):
    if current_client.typ != "client":
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="you are not a client")
    if not current_client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")
    return current_client
