from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .routes import clients, authors, users, admin, books, purchase
from . import auth

from app.database import get_db, run_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_generator = get_db()
    db = await anext(db_generator)
    try:
        app.state.n_client = await run_redis()
        await db.execute(text("create extension if not exists btree_gist;"))
        await db.commit()
        yield
    finally:
        await db.close()
        await app.state.n_client.close()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(clients.router)
app.include_router(authors.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(purchase.router)
