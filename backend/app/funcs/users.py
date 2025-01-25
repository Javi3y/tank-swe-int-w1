from .. import models


async def add_user(user, db, typ):
    new_user = models.User(**user.model_dump())
    new_user.typ = typ
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
