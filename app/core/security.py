from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.token import TokenData
from app.core.settings import get_settings

settings = get_settings()


# Password cryptography
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class APIKeyCookieCustom(APIKeyCookie):
    """
    Custom APIKeyCookie
    """

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Override that returns None instead of raising an exception if there is no key
        """
        api_key: str = request.cookies.get(self.model.name)
        if not api_key:
            return None
        return api_key


class OAuth2PasswordBearerCustom(OAuth2PasswordBearer):
    """ Custom OAuth2PasswordBearer """

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Override that returns None instead of raising an exception
        """
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                return None
        return param


cookie_session = APIKeyCookieCustom(name="session")
oauth2_scheme = OAuth2PasswordBearerCustom(tokenUrl="authentication/login")


class Hashing:
    """
    Class Hashing
    """

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Returns the password encrypted
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(login_password: str, user_password: str) -> bool:
        """
        Verifies the login password
        """
        return pwd_context.verify(login_password, user_password)


class Oauth2:
    """
    Authentication class
    """

    OAUTH2_SECRET_KEY = settings.oauth2_secret_key
    OAUTH2_ALGORITHM = settings.oauth2_algorithm
    OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES = settings.oauth2_access_token_expire_minutes

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates the access token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.OAUTH2_SECRET_KEY, algorithm=cls.OAUTH2_ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_token(cls, token: str, credentials_exception) -> TokenData:
        """
        Verifies the token
        """
        try:
            payload = jwt.decode(token, cls.OAUTH2_SECRET_KEY, algorithms=[cls.OAUTH2_ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            return TokenData(username=email)
        except JWTError:
            raise credentials_exception




