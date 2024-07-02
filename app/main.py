from core.fastapi_configs import FastAPIConfigs
from dependencies import auth_api_key
from fastapi import FastAPI, Security
from routers.root import router

app = FastAPI(
    # docs_url=None,  # Comment out these two codes with option docs_url, redoc_url if you want to disable api documentations
    # redoc_url=None,
    lifespan=FastAPIConfigs.lifespan,
    dependencies=[Security(auth_api_key)],
)

FastAPIConfigs(app)  # define lifespan, exception handlers

# Prevent 307 Temporary Redirect due to '/' at the end of endpoint
# app.router.redirect_slashes = False

app.include_router(router)


@app.get("/")
async def root():
    return {"msg": "main page"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
# Launch this server with command "uvicorn app.main:app --host 0.0.0.0 --port 8000" from source directory of this repository
