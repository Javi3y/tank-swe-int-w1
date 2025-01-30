from typing import List
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from app.models import users
from app.services.clients import ClientService, get_client_service
from app.services.purchase import PurchaseService, get_purchase_service


router = APIRouter(prefix="/purchase", tags=["Purchases"])


# Done
@router.post("/",response_model=schemas.ReservationOut)
async def reserve(
    reservation: schemas.ReservationIn,
    current_client: users.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    client_service: ClientService = Depends(get_client_service),
    purchase_service: PurchaseService = Depends(get_purchase_service),
):
    new_reservation = await purchase_service.reserve(
        current_client, reservation.book_id, client_service, db
    )
    return new_reservation


## I know that this isn't the right place will fix later! :D
# @router.post("/subscribe")
# async def subscribe(
#    current_client: users.User = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
#    purchase_service: PurchaseService = Depends(get_purchase_service),
#    client_service: ClientService = Depends(get_client_service),
# ):
#    sub = await purchase_service.purchase_subscription(
#        current_client, "plus", client_service, db
#    )
#    return {"sub": sub}
#
#
# @router.get("/subscription")
# async def subscription(
#    current_client: users.User = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
#    client_service: ClientService = Depends(get_client_service),
# ):
#    return await client_service.get_subscription(current_client, db)
