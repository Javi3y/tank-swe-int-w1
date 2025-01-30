from datetime import UTC, datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
)

from app.models import books, purchase, users
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
        sub = await db.execute(
            select(users.Subscription)
            .where(users.Subscription.client_id == client.id)
            .order_by(users.Subscription.sub_end.desc())
        )
        sub = sub.scalar()
        if not sub:
            date = datetime.now(UTC)
        else:
            date = sub.sub_end if sub.sub_end > datetime.now(UTC) else datetime.now(UTC)

        subscription = users.Subscription(
            client=client,
            subscription_model=typ,
            sub_start=date,
            sub_end=date + timedelta(days=30),
        )
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        return subscription

    async def reserve(
        self, client_id, book_id, client_service: ClientService, db: AsyncSession
    ):
        client = await client_service.get_item(client_id, db)
        sub = await client_service.get_subscription(client_id, db)
        if not sub:
            raise HTTPException(
                HTTP_403_FORBIDDEN, detail="user must have atleast a plus subscription"
            )
        prev_reservations = await self.get_reservations(client.id, db)
        await self.can_reserve(sub.typ.value, prev_reservations)
        can_reserve = self.can_reserve(book_id, db)
        if can_reserve:
            #reserve
            pass
        else :
            #add in queue
            pass
        return

    async def get_reservations(self, client_id, db: AsyncSession):
        reservations = await db.execute(
            select(purchase.Reservation).where(
                purchase.Reservation.client_id == client_id
            )
        )
        return reservations

    async def can_reserve(self, typ, reservations):
        reservations_count = len(reservations.all())
        if typ == 2:
            if reservations_count >= 5:
                raise HTTPException(
                    HTTP_403_FORBIDDEN, detail="you can't reserve any more books"
                )
        if typ == 3:
            if reservations_count >= 10:
                raise HTTPException(
                    HTTP_403_FORBIDDEN, detail="you can't reserve any more books"
                )

    async def can_reserve(self, book, db):
        book = await db.execute(select(books.Book).where(books.Book_id==book))
        return True if book.scalar().units > 0 else False
            


async def get_purchase_service() -> PurchaseService:
    return PurchaseService()
