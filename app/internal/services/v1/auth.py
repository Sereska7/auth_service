"""Models for Auth object."""

from logging import Logger
from jose import jwt

from app.internal.pkg.jwt.jwt_handler import JWTHandler
from app.internal.pkg.password.password import check_password
from app.internal.repository.v1.postgresql.user import UserRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.auth import UserInactive, InvalidCredentials, InvalidTokenPayload, \
    InvalidAuthCredentials, TokenPayloadMissingUserID
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult
from app.pkg.models.v1.exceptions.user import UserReadError, UserNotFound
from app.pkg.settings import settings

__all__ = ["AuthService"]


class AuthService:
    """Auth service class."""

    user_repository: UserRepository
    jwt_handler: JWTHandler
    __logger: Logger = get_logger(__name__)

    async def authenticate_user(
        self,
        cmd: models.UserAuthCommand
    ) -> models.TokenResponse:
        """
        Authenticates a user using email and password, then returns access and refresh tokens.

        Args:
            cmd (models.UserAuthCommand): Command object containing user credentials (email and password).

        Returns:
            models.TokenResponse: Contains access token, refresh token, and token type.
        """

        user = await self.user_repository.get_user_by_email(cmd)

        if not user:
            raise InvalidCredentials

        if not check_password(cmd.user_password, user.hashed_password):
            raise InvalidCredentials

        if not user.user_is_active:
            raise UserInactive

        access_token = self.jwt_handler.create_access_token({"user_id": str(user.user_id)})
        refresh_token = self.jwt_handler.create_refresh_token({"user_id": str(user.user_id)})

        return models.TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_access_token(self, refresh_token: str) -> models.TokenResponse:
        """
        Refreshes the access token using a valid refresh token.

        Args:
            refresh_token (str): The refresh token string provided by the client.

        Returns:
            models.TokenResponse: Contains new access and refresh tokens with token type.
        """

        payload = jwt.decode(
            refresh_token,
            settings.JWT.REFRESH_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT.ALGORITHM],
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise InvalidTokenPayload

        user = await self.user_repository.get_user_by_id(
            cmd=models.UserReadByIDCommand(user_id=user_id)
        )
        if not user or not user.user_is_active:
            raise UserNotFound

        access_token = self.jwt_handler.create_access_token({"user_id": str(user_id)})
        refresh_token = self.jwt_handler.create_refresh_token({"user_id": str(user_id)})

        return models.TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


    async def get_current_user(
        self,
        token: str
    ) -> models.User:
        """
        Retrieves the current user based on the provided access token.

        Args:
            token (str): The JWT access token.

        Returns:
            models.User: The full user data retrieved from the repository.
        """

        payload = self.jwt_handler.decode_access_token(token)
        if payload is None:
            raise InvalidAuthCredentials

        user_id = payload.get("user_id")
        if user_id is None:
            raise TokenPayloadMissingUserID

        try:
            user = await self.user_repository.get_full_user_by_id(
                cmd=models.UserReadByIDCommand(user_id=user_id)
            )
            return user
        except DriverError as exc:
            raise UserReadError from exc
        except EmptyResult as exc:
            raise UserNotFound from exc
