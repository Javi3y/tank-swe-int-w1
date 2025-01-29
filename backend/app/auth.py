from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from . import schemas
from .config import settings
from .database import get_db
from .models import users

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded, expire


async def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        db_generator = get_db()
        db = await anext(db_generator)
        try:
            user = await db.execute(select(users.User).where(users.User.id == id))
            user = user.scalar()
            if not user.token_expire:
                raise credentials_exception
        finally:
            await db.close()

    except JWTError:
        raise credentials_exception
    return token_data



async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"www-Authenticate": "Bearer"},
    )
    try:
        raw_token = request.headers.get("Authorization")
        if not raw_token:
            raise credentials_exception
        scheme, token = raw_token.split()
        if scheme.lower() != "bearer":
            raise credentials_exception
    except ValueError:
        raise credentials_exception

    user_token = await verify_access_token(token, credentials_exception)
    results = await db.execute(select(users.User).where(users.User.id == user_token.id))
    return results.scalar()


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
async def login(
    user_credentials: schemas.Auth,
    db: AsyncSession = Depends(get_db),
):
    results = await db.execute(
        select(users.User).where(
            (users.User.username == user_credentials.username)
            | (users.User.email == user_credentials.username)
        )
    )
    user = results.scalar()
    if not user or not user_credentials.password == user.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="invalid credentails"
        )
    access_token, expire = await create_access_token(data={"user_id": user.id})
    user.token_expire = expire

    await db.commit()
    await db.refresh(user)


    return {"access_token": access_token, "token_type": "bearer"}

#@router.post("/opt")
#async def verify_otp(user_credentials: schemas.Auth,otp:int, db: AsyncSession):
#    pass
