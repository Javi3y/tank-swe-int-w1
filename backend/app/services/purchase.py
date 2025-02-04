from datetime import UTC, datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from app.models import books, purchase, users
from app.services.clients import ClientService
from app.services.books import BookService


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

    async def add_balance(self, client, amount, db: AsyncSession):
        client = await db.execute(
            select(users.Client).where(users.Client.id == client.id)
        )
        client = client.scalar()
        if not client:
            raise HTTPException(HTTP_404_NOT_FOUND)
        client.balance += amount
        await db.commit()
        await db.refresh(client)
        return client

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
        await self.can_reserve(sub.subscription_model.value, prev_reservations)
        can_reserve = await self.reserve_or_queue(book_id, db)
        if can_reserve:
            return await self.create_reservation(book_id, client.id, db)
        else:
            return await self.create_reservation_queue(book_id, client.id, db)

    async def get_reservations(self, client_id, db: AsyncSession):
        reservations = await db.execute(
            select(purchase.Reservation).where(
                purchase.Reservation.client_id == client_id
            )
        )
        return reservations.scalars()

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

    async def reserve_or_queue(self, book, db):
        book = await db.execute(select(books.Book).where(books.Book.id == book))
        book = book.scalar()
        if not book:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return True if book.units > 0 else False

    async def create_reservation(self, book, client, db):
        new_reservation = purchase.Reservation(book_id=book, client_id=client)
        db.add(new_reservation)
        await db.commit()
        await db.refresh(new_reservation)
        book_unit = await db.execute(select(books.Book).where(books.Book.id == book))
        book_unit = book_unit.scalar()
        book_unit.units -= 1
        await db.commit()
        await db.refresh(book_unit)
        await db.refresh(new_reservation)
        return new_reservation

    async def create_reservation_queue(self, book, client, db):
        new_reservation_queue = purchase.ReservationQueue(
            book_id=book, client_id=client
        )
        db.add(new_reservation_queue)
        await db.commit()
        await db.refresh(new_reservation_queue)
        return new_reservation_queue

    async def get_latest_in_queue(self, book_id, db):
        query = await db.execute(
            text(
                f"""
            WITH RankedReservations AS (
                SELECT
                    rq.id,
                    rq.book_id,
                    rq.client_id,
                    s.subscription_model,
                    rq.created_at,
                    ROW_NUMBER() OVER (
                        PARTITION BY rq.book_id
                        ORDER BY
                            CASE
                                WHEN s.subscription_model = 'premium' THEN 1
                                WHEN s.subscription_model = 'plus' THEN 2
                                ELSE 3
                            END,
                            rq.created_at
                    ) AS rank
                FROM reservation_queue rq
                JOIN client c ON rq.client_id = c.id
                JOIN subscription s ON c.id = s.client_id
            )
            SELECT id, book_id, client_id, subscription_model, created_at  -- Include id here
            FROM RankedReservations
            WHERE rank = { book_id }
            """
            )
        )
        result = query.fetchone()
        reservations = {
                "id": result.id,
                "book_id": result.book_id,
                "client_id": result.client_id,
                "subscription_model": result.subscription_model,
                "created_at": result.created_at,
            }
        
        return reservations

    async def resolve_reservation_queue(self, client_service: ClientService, book, db):
        reservation = await self.get_latest_in_queue(book, db)
        print(reservation)
        prev_reservations = await self.get_reservations(reservation["client_id"], db)
        client = await client_service.get_item(reservation["client_id"], db)
        try:
            await self.can_reserve(client.current_subscription, prev_reservations)
        except HTTPException as e:
            raise e
        return reservation


async def get_purchase_service() -> PurchaseService:
    return PurchaseService()
