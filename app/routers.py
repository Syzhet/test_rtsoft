from typing import Union

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from db.crud import ReqouestToDB
from db.schemas.schemas import QueryParametr

router: APIRouter = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    session: AsyncSession = Depends(get_session),
    category: QueryParametr = Depends()
):
    request_to_db = ReqouestToDB(
        session,
        category.model_dump().get('category')
    )
    data = await request_to_db.get_data()
    return templates.TemplateResponse(
        "response.html",
        {"request": request, "data": data}
    )


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
