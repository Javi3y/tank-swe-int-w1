from typing import List
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/books", tags=["Books"])


async def check_admin(user):
    print(user.typ)
    print(models.Typ("admin"))
    if user.typ != models.Typ("admin") and user.typ != models.Typ("author"):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="user doesn't have the permisions for this operation")


@router.post("/")
async def create_book(book: schemas.Book, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    await check_admin(current_user) 
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return {"book": new_book.title}


@router.get("/", response_model=List[schemas.Book])
async def get_books(db: Session = Depends(get_db)):
    books = await db.execute(select(models.Book))
    return books.scalars().all()
#
#
#@router.patch("/", response_model=schemas.ClientOut)
#async def update_client(
#    updated_client: schemas.ClientUpdate,
#    current_client: int = Depends(get_current_user),
#    db: Session = Depends(get_db),
#):
#    if not client:
#        raise HTTPException(HTTP_404_NOT_FOUND, detail="client does not exist")
#
#    client = current_client
#
#    client_dict = updated_client.model_dump(exclude_none=True)
#
#    for key, value in client_dict.items():
#        setattr(client, key, value)
#
#    await db.commit()
#    await db.refresh(client)
#    return client
#
#
#@router.delete("/")
#async def delete_client(
#    current_client: models.User = Depends(get_current_user),
#    db: Session = Depends(get_db),
#):
#    if not current_client:
#        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")
#
#    await db.delete(current_client)
#    await db.commit()
#    return Response(status_code=HTTP_204_NO_CONTENT)
#
#
#@router.get("/profile", response_model=schemas.ClientOut)
#async def get_profile(current_client: int = Depends(get_current_user)):
#    if current_client.typ != "client":
#        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="you are not a client")
#    if not current_client:
#        raise HTTPException(HTTP_404_NOT_FOUND, detail="client doesn't exist")
#    return current_client
