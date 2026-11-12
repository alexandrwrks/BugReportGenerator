from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.response_schema import BugReport
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    title="Bag Report Generator API",
    version="0.1.0",
    lifespan=lifespan
)

default_openapi = app.openapi

def custom_openapi():
    schema = default_openapi()
    schemas = schema.setdefault("components", {}).setdefault("schemas", {})
    if "BugReport" not in schemas:
        schemas["BugReport"] = BugReport.model_json_schema(mode="serialization")
    return schema

app.openapi = custom_openapi

app.include_router(router)