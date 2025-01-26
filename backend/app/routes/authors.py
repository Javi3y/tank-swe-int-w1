from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/authors", tags=["Authors"])


# @router.post("/")
# async def create_author(author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)):
#    new_author = models.Author(**author.model_dump())
#    city = await db.execute(
#        select(models.City).where(models.City.id == new_author.city)
#    )
#    new_author.city = city.scalar()
#    db.add(new_author)
#    await db.commit()
#    await db.refresh(new_author)
#    return {"author": new_author.email}


@router.get("/", response_model=List[schemas.AuthorOut])
async def get_authors(db: AsyncSession = Depends(get_db)):
    authors = await db.execute(select(models.Author))
    return authors.scalars().all()


# @router.patch("/", response_model=schemas.AuthorOut)
# async def update_author(
#    updated_author: schemas.AuthorUpdate,
#    current_author: int = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
# ):
#    author = current_author
#
#    author_dict = updated_author.model_dump(exclude_none=True)
#
#    for key, value in author_dict.items():
#        setattr(author, key, value)
#
#    await db.commit()
#    await db.refresh(author)
#    return author
#
#
# @router.delete("/")
# async def delete_author(
#    current_author: models.User = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
# ):
#    await db.delete(current_author)
#    await db.commit()
#    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.AuthorOut)
async def get_profile(
    current_author: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if current_author.typ != models.Typ("author"):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="you are not an author")
    author = await db.execute(
        select(models.Author)
        .where(models.Author.id == current_author.id)
        .options(selectinload(models.Author.city))
    )
    return author.scalar()
