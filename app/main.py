import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse

from app.routers import router
from config.config import base_config

app: FastAPI = FastAPI()

app.include_router(
    router=router,
    prefix='/api/v1'
)


@app.exception_handler(ValueError)
async def validation_exception_handler(
    request, exc: ValueError
) -> PlainTextResponse:
    """Обработка исключений при валидации передаваемых параметров запроса."""

    return PlainTextResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=str(exc).split('\n')[2]
    )

if __name__ == '__main__':
    uvicorn.run(
        app, host=base_config.app.app_host,
        port=base_config.app.app_port
    )
