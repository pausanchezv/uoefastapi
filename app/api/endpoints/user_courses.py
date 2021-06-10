import logging
from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app import crud
from app import models
from app import schemas
from app.api.dependencies import get_db


logger = logging.getLogger("user_courses")

router = APIRouter()


@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCourseResponse)
def add_course_to_user(user_request: schemas.UserCourseRequest, db: Session = Depends(get_db)):
    """
    Adds a course to a user
    """

    user = db.query(models.User).filter(models.User.id == user_request.user_id).first()
    course = crud.course.get(db, obj_id=user_request.course_id)

    if not user or not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object does not exist')

    try:

        user.courses.append(course)
        db.commit()

        last_inserted_object = db.query(models.UserCourses).filter(
            models.UserCourses.user_id == user.id,
            models.UserCourses.course_id == course.id
        ).first()

        return last_inserted_object

    except Exception as error:
        logger.error(f'Error when adding a course to a user: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.delete('/remove', status_code=status.HTTP_204_NO_CONTENT)
def remove_course_from_user(user_request: schemas.UserCourseRequest, db: Session = Depends(get_db)):
    """
    Removes a course from a user
    """

    course = crud.course.get(db, obj_id=user_request.course_id)
    user = db.query(models.User).filter(models.User.id == user_request.user_id).first()

    if not user or not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object does not exist')

    try:

        user.courses.remove(course)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as error:
        logger.error(f'Error when removing a course from a user: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.delete('/remove-all/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_all_courses_from_user(user_id: int, db: Session = Depends(get_db)):
    """
    Removes all the courses from a user
    """

    try:

        user = db.query(models.User).filter(models.User.id == user_id).first()

        if user:
            user.courses = []
            db.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object does not exist')

    except Exception as error:
        logger.error(f'Error when removing a course from a user: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

