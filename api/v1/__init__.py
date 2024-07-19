from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from settings import NAME
from utils.errors import __validation_exception_handler

from .app import router as app_router
from .generated import router as generated_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    return __validation_exception_handler(exc)


app.include_router(app_router)
app.include_router(generated_router)


@app.get("/ping")
async def ping_handler() -> str:
    """Return string if service is alive"""
    return f"Ping service {NAME}"
