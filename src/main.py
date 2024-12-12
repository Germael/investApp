from fastapi import FastAPI

from route.parsing_route import parse_router

app = FastAPI()


app.include_router(parse_router)


@app.get("/healthcheck")
def health_check():
    return "healthy"
