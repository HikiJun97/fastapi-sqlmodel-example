from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import Config

DATABASE_URL = f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DATABASE}"
async_engine = create_async_engine(DATABASE_URL, echo=True)
