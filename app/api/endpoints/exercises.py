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

logger = logging.getLogger("exercises")

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    """
    Obtains all the exercises
    """

    exercises: List[models.UseOfEnglishExercise] = crud.exercise.get_multi(db, skip=0, limit=100)
    return exercises


@router.get("/open-cloze", status_code=status.HTTP_200_OK, response_model=List[schemas.OpenClozeResponse])
def get_open_cloze(db: Session = Depends(get_db)):
    """
    Obtains all the open cloze exercises
    """

    exercises = db.query(models.OpenCloze).all()
    return exercises


@router.get("/keyword-transformation", status_code=status.HTTP_200_OK, response_model=List[schemas.KWTransformationResponse])
def get_open_cloze(db: Session = Depends(get_db)):
    """
    Obtains all the Use of English exercises
    """

    exercises = db.query(models.KeywordTransformation).all()
    return exercises


@router.get("/{exercise_id}", status_code=status.HTTP_200_OK, response_model=schemas.ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Obtains an exercise by id
    """

    exercise = db.query(models.UseOfEnglishExercise).filter(models.UseOfEnglishExercise.id == exercise_id).first()

    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Exercise {exercise_id} not found')

    return exercise


@router.get("/open-cloze/{exercise_id}", status_code=status.HTTP_200_OK, response_model=schemas.OpenClozeResponse)
def get_open_cloze(exercise_id: int, db: Session = Depends(get_db)):
    """
    Obtains all the open cloze exercises
    """

    exercise = db.query(models.OpenCloze).filter(models.OpenCloze.id == exercise_id).first()

    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Exercise {exercise_id} not found')

    return exercise


@router.post("/open_cloze", status_code=status.HTTP_201_CREATED, response_model=schemas.OpenClozeResponse)
def create_open_cloze(exercise_request: schemas.OpenClozeRequest, db: Session = Depends(get_db)):
    """
    Creates an exercise and stores it to the database
    """

    try:
        return crud.open_cloze.create_open_cloze(db, obj_in=exercise_request)

    except Exception as error:
        logger.error(f'Error when creating an open cloze: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.post("/keyword_transformation", status_code=status.HTTP_201_CREATED, response_model=schemas.KWTransformationResponse)
def create_kw_transformation(exercise_request: schemas.KWTransformationRequest, db: Session = Depends(get_db)):
    """
    Creates an exercise and stores it to the database
    """

    try:
        return crud.keyword_transformation.create_keyword_transformation(db, obj_in=exercise_request)

    except Exception as error:
        logger.error(f'Error when creating an open cloze: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Deletes an exercise form the database
    """

    obj = db.query(models.UseOfEnglishExercise).get(exercise_id)
    db.delete(obj)
    db.commit()

    # try:
    #     crud.exercise.delete(db, obj_id=exercise_id)
    # except Exception as error:
    #     logger.error(f'{error}')
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

    return Response(status_code=status.HTTP_204_NO_CONTENT)