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
from app.services.purchase import PurchaseService, get_purchase_service


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


# Done
@router.patch("/", response_model=schemas.ClientOut)
async def update_client(
    updated_client: schemas.ClientUpdate,
    current_client: int = Depends(get_current_user),
    client_service: ClientService = Depends(get_client_service),
    db: AsyncSession = Depends(get_db),
):
    return await client_service.update_item(updated_client, current_client, db)


@router.delete("/")
async def delete_client(
    current_client: users.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    client_service: ClientService = Depends(get_client_service),
):
    return await client_service.delete_item(current_client, db)


# Done
@router.get("/profile", response_model=schemas.ClientOut)
async def get_profile(
    client_service: ClientService = Depends(get_client_service),
    current_client: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await client_service.get_item(current_client, db)


# I know that this isn't the right place will fix later! :D
@router.post("/subscribe")
async def subscribe(
    current_client: users.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    purchase_service: PurchaseService = Depends(get_purchase_service),
    client_service: ClientService = Depends(get_client_service),
):
    sub = await purchase_service.purchase_subscription(
        current_client, "plus", client_service, db
    )
    return {"sub": sub}
