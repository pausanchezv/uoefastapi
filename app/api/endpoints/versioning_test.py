import logging
import os
import sys
from typing import List

from fastapi import APIRouter, Depends
from fastapi_versioning import VersionedFastAPI, version

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app import crud
from app import models
from app import schemas
from app.api.dependencies import get_db

logger = logging.getLogger("versioning_test")

router = APIRouter()


@router.get("/test1")
@version(1, 0)
def test():
    return {"test": "1.0"}


@router.get("/test")
@version(1, 1)
def test():
    return {"test": "1.1"}


@router.get("/test1")
@version(2, 0)
def test():
    return {"test": "2.0"}