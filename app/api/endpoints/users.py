import logging
from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from app import models
from app import schemas
from app.api.dependencies import get_current_user, get_db
from app.core.security import Hashing


logger = logging.getLogger("users")

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """
    Obtains all the users
    """
    users = db.query(models.User).all()
    return users


@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(current_user: models.User = Depends(get_current_user)):
    """
    Obtains all the Use of English courses
    """
    return current_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)): # , _: models.User = Depends(get_current_user)
    """
    Obtains a user by id
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user} not found')

    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_request: schemas.UserRequest, db: Session = Depends(get_db)):

    # todo: use crud here

    user = models.User(
        name=user_request.name,
        email=user_request.email,
        password=Hashing.get_password_hash(user_request.password),
        is_superuser=user_request.is_superuser
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception as error:
        logger.error(f'Error when creating a user: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{error}')

    return user