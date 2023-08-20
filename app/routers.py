from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from db.crud import ReqouestToDB
from db.schemas.schemas import QueryParametr

router: APIRouter = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
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


@router.get(
    "/health-check",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK
)
def health_check():
    return 'Application: OK'
