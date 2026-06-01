from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..database import engine, Base
from routers import registration


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(
    registration.router, prefix="/api/v0/registration", tags=["registration"]
)
