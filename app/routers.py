from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import Image
from db.base import get_session

router: APIRouter = APIRouter()


@router.get("/")
async def read_root(session: AsyncSession = Depends(get_session)):
    data = await session.get(Image, 1)
    return {"Hello": f"{data}"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
