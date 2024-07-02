from contextlib import asynccontextmanager

from core.database.engine import async_engine, create_table
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class FastAPIConfigs:
    def __new__(cls, app: FastAPI):
        ExceptionHandlers(app)

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        await create_table(async_engine)
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
