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

logger = logging.getLogger("activities")

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    """
    Obtains all the Use of English activities
    """
    return crud.activity.get_multi(db, skip=0, limit=100)


@router.get("/{activity_id}", status_code=status.HTTP_200_OK, response_model=schemas.ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Obtains an activity by id
    """
    # activity = db.query(models.UseOfEnglishActivity).filter(models.UseOfEnglishActivity.id == activity_id).first()
    activity = crud.activity.get(db, obj_id=activity_id)

    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Activity {activity_id} not found')

    return activity


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ActivityResponse)
def create_activity(activity_request: schemas.ActivityRequest, db: Session = Depends(get_db)):
    """
    Creates an activity and stores it to the database
    """
    try:
        return crud.activity.create(db, obj_in=activity_request)

    except Exception as error:
        logger.error(f'Error when creating an activity: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.put("/{activity_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ActivityResponse)
def update_activity(activity_id: int, activity_request: schemas.ActivityRequest, db: Session = Depends(get_db)):
    """
    Updates an activity
    """

    activity = crud.activity.get(db, obj_id=activity_id)

    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Activity {activity} not found')

    try:
        print({**activity_request.dict()})
        print(activity_request.__dict__)
        return crud.activity.update(db, db_obj=activity, obj_in={**activity_request.dict()})
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.patch("/{activity_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ActivityResponse)
def partial_update_activity(activity_id: int, activity_request: schemas.ActivityRequestPartial, db: Session = Depends(get_db)):
    """
    Updates ana activity (partially)
    """
    activity = crud.activity.get(db, obj_id=activity_id)

    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Activity {activity} not found')

    try:
        return crud.activity.update(db, db_obj=activity, obj_in=activity_request)
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(activity_id: int, db: Session = Depends(get_db)):
    """
    Deletes an activity form the database
    """
    try:
        crud.activity.delete(db, obj_id=activity_id)
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

    return Response(status_code=status.HTTP_204_NO_CONTENT)