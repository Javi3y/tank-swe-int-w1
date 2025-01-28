from datetime import UTC, datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_402_PAYMENT_REQUIRED

from app.models import users
from app.services.clients import ClientService


class PurchaseService:
    prices_dict = {"plus": 50000, "premium": 200000}

    async def purchase_subscription(
        self, client, typ, client_service: ClientService, db: AsyncSession
    ):
        if typ not in self.prices_dict.keys():
            raise HTTPException(HTTP_400_BAD_REQUEST, "Subscription model not found")
        price = self.prices_dict[typ]
        client = await client_service.get_item(client, db)
        if client.balance < price:
            raise HTTPException(HTTP_402_PAYMENT_REQUIRED, "Balance is insufficient")
        client.balance = client.balance - price

        await db.commit()
        await db.refresh(client)
        return await self.create_subscription(client, typ, db)

    async def create_subscription(self, client, typ, db: AsyncSession):
        subscription = users.Subscription(
            client=client,
            subscription_model=typ,
            start=datetime.now(UTC),
            end=datetime.now(UTC) + timedelta(days=30),
        )
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        return subscription


async def get_purchase_service() -> PurchaseService:
    return PurchaseService()
