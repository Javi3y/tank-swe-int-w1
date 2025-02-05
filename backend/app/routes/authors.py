from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from app import schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends
from app.repository.authors import AuthorRepository
from app.services.author import get_author_service, AuthorService
from app.unit_of_work.uow import UnitOfWork

router = APIRouter(prefix="/authors", tags=["Authors"])

def get_uow(repo_cls):
    async def _get_uow(db: AsyncSession = Depends(get_db)) -> UnitOfWork:
        return UnitOfWork(db, repo_cls)
    return Depends(_get_uow)

# @router.post("/")
# async def create_author(author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)):
#    new_author = users.Author(**author.model_dump())
#    city = await db.execute(
#        select(users.City).where(users.City.id == new_author.city)
#    )
#    new_author.city = city.scalar()
#    db.add(new_author)
#    await db.commit()
#    await db.refresh(new_author)
#    return {"author": new_author.email}


@router.get("/", response_model=List[schemas.AuthorOut])
async def get_authors(
    author_service: AuthorService = Depends(get_author_service),
    uow: UnitOfWork = get_uow(AuthorRepository)
):
    return await author_service.get_items(uow)


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
#    current_author: users.User = Depends(get_current_user),
#    db: AsyncSession = Depends(get_db),
# ):
#    await db.delete(current_author)
#    await db.commit()
#    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/profile", response_model=schemas.AuthorOut)
async def get_profile(
    current_author: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    author_service: AuthorService = Depends(get_author_service),
):
    return await author_service.get_item(current_author.id, db)
