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
from app.api.dependencies import get_current_user, get_current_active_superuser, get_db

logger = logging.getLogger("courses")

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):  # , _: models.User = Depends(get_current_user))
    """
    Obtains all the courses
    """
    return crud.course.get_multi(db, skip=0, limit=100)


@router.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=schemas.CourseResponseWithUsers)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtains a course by id
    """
    course = crud.course.get(db, obj_id=course_id)

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course {course_id} not found')

    return schemas.CourseResponseWithUsers(
        name=course.name,
        level=course.level,
        description=course.description,
        background_color=course.background_color,
        activities=course.activities,
        users=course.users.all()
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CourseResponse)
def create_course(course_request: schemas.CourseRequest, db: Session = Depends(get_db)):
    """
    Creates a course and stores it to the database
    """

    try:
        course = crud.course.create(db, obj_in=course_request)

    except Exception as error:
        logger.error(f'Error when creating a course: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

    return course


@router.put("/{course_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.CourseResponse)
def update_course(course_id: int, course_request: schemas.CourseRequest, db: Session = Depends(get_db)):
    """
    Updates a course
    """

    course = crud.course.get(db, obj_id=course_id)

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course {course_id} not found')

    try:
        return crud.course.update(db, db_obj=course, obj_in=course_request.__dict__)
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.patch("/{course_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.CourseResponse)
def partial_update_course(course_id: int, course_request: schemas.CourseRequestPartial, db: Session = Depends(get_db)):
    """
    Updates a course (partially)
    """

    course = crud.course.get(db, obj_id=course_id)

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course {course_id} not found')

    try:
        return crud.course.update(db, db_obj=course, obj_in=course_request)
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Deletes a course form the database
    """

    try:
        crud.course.delete(db, obj_id=course_id)
    except Exception as error:
        logger.error(f'{error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

