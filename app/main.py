import asyncio
import logging
import random
import time

import aiohttp
import uvicorn
from fastapi import FastAPI, Depends
from fastapi_versioning import VersionedFastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware


from app import models
from app.api.dependencies import get_db
from app.core import settings, app_logger

from app.api.router import api_router

logger = logging.getLogger("main")


app = FastAPI(
    # openapi_url="/api/v1/openapi.json",
    title=settings.get_settings().app_name,
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0",
)

app.include_router(api_router)

app = VersionedFastAPI(
    app=app,
    prefix_format="/api/v{major}_{minor}",
    default_api_version=(1, 0)
)

if settings.get_settings().backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_settings().backend_cors_origins.split(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Off because the database is created by running migrations
# Base.metadata.create_all(bind=engine)


@app.get("/")
def main():
    """
    Main Application Page
    """
    return {'FastApi': 'UOE PRO'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # , reload=True
