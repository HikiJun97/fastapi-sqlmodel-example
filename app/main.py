from fastapi import FastAPI, HTTPException, Security
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.routers.main import router
from contextlib import asynccontextmanager
from app.core.database.engine import async_engine
from app.dependencies import auth_api_key
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan, dependencies=[Security(auth_api_key)])
app.router.redirect_slashes = (
    False  # 엔드포인트 끝의 '/'로 인한 307 Temporary Redirect 방지
)
app.include_router(router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


@app.get("/")
async def root():
    return {"msg": "main page"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
