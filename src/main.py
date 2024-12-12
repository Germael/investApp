from fastapi import FastAPI

from route.info_route import info_router
from route.parsing_route import parse_router

app = FastAPI()


app.include_router(info_router)
app.include_router(parse_router)


@app.get("/healthcheck")
def health_check():
    return "healthy"
