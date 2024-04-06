from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.database.engine import async_engine
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


class FastAPIConfigs:
    def __new__(cls, app: FastAPI):
        ExceptionHandlers(app)

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        yield
        await async_engine.dispose()


class ExceptionHandlers:
    def __new__(cls, app: FastAPI):
        @app.exception_handler(HTTPException)
        async def fastapi_http_exception_handler(request, exc):
            return await http_exception_handler(request, exc)

        @app.exception_handler(StarletteHTTPException)
        async def custom_http_exception_handler(request, exc):
            return await http_exception_handler(request, exc)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return await request_validation_exception_handler(request, exc)
