import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from route.info_route import info_router
from route.parsing_route import parse_router


DB_FILE_PATH = "app/db/invest.db"


@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    #TODO: remove when alembic added
    if os.path.exists(DB_FILE_PATH):
        os.remove(DB_FILE_PATH)
        print(f"Deleted file: {DB_FILE_PATH}")
    else:
        print(f"File does not exist: {DB_FILE_PATH}")

    yield

    print("Application shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(info_router)
app.include_router(parse_router)


@app.get("/healthcheck")
def health_check():
    return "healthy"
