""" """

from datetime import datetime, timedelta, timezone
from logging import Logger

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.internal.repository.v1.postgresql import UserRepository
from app.pkg.logger import get_logger
from app.pkg.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


class JWTHandler:
    """ """

    user_repository: UserRepository
    __logger: Logger = get_logger(__name__)

    @staticmethod
    def _create_token(
        data: dict,
        expires_delta: timedelta,
        secret_key: str,
        algorithm: str,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        return JWTHandler._create_token(
            data=data,
            expires_delta=expires_delta
            or timedelta(minutes=settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES),
            secret_key=settings.JWT.SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
        return JWTHandler._create_token(
            data=data,
            expires_delta=expires_delta or timedelta(days=settings.JWT.REFRESH_TOKEN_EXPIRE_DAYS),
            secret_key=settings.JWT.REFRESH_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.ALGORITHM,
        )

    @staticmethod
    def decode_access_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT.SECRET_KEY.get_secret_value(),
                algorithms=[settings.JWT.ALGORITHM],
            )
            return payload
        except JWTError:
            return None
