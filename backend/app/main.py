from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from .routes import clients, authors, users
from . import auth

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(authors.router)
app.include_router(auth.router)
