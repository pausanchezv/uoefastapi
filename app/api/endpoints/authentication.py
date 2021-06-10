import logging

from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from app import models
from app import schemas
from app.api.dependencies import get_db

from app.core.security import Hashing, Oauth2

logger = logging.getLogger("authentication")

router = APIRouter()


@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(response: Response, login_request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Logs the user in with JWT Token
    """

    user = db.query(models.User).filter(models.User.email == login_request.username).first()

    if not user or not Hashing.verify_password(login_request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid credentials')

    access_token_expires = timedelta(minutes=Oauth2.OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Oauth2.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response.set_cookie("session", access_token)  # Testing

    return {"access_token": access_token, "token_type": "bearer"}
