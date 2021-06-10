from typing import Optional

from fastapi import Depends, HTTPException, status


from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import app.models as models
from app.core import security
from app.core.database import SessionLocal

from app.core.security import cookie_session


def get_db():
    """ Yields the database instance """

    db: Optional[SessionLocal] = None

    try:
        db = SessionLocal()
        yield db

    finally:
        if db is not None:
            db.close()


async def get_current_user(db: Session = Depends(get_db), header_token: Optional[str] = Depends(security.oauth2_scheme),
                           session_token: Optional[str] = Depends(cookie_session)):
    """
    Obtains the currently authenticated user
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token: str = header_token or session_token

    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"},)

    token_data = security.Oauth2.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)) -> models.User:
    """
    Returns the current active user
    """
    if not db.query(models.User).filter(models.User.id == user.id, models.User.is_active).first():
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_active_superuser(db: Session = Depends(get_db), user: models.User = Depends(get_current_active_user)) -> models.User:
    """
    Returns the current active superuser
    """
    if not db.query(models.User).filter(models.User.id == user.id, models.User.is_superuser).first():
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user