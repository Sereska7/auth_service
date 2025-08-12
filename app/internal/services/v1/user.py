"""Models for User object."""

from logging import Logger

from passlib.handlers.bcrypt import bcrypt

from app.internal.pkg.middlewares.verification_email import VerifyEmail
from app.internal.pkg.password.password import check_password
from app.internal.repository.v1.postgresql.user import UserRepository
from app.pkg.clients.v1.notification_service import NotificationServiceClient
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.auth import InvalidCredentials
from app.pkg.models.v1.exceptions.repository import (
    DriverError,
    EmptyResult,
    UniqueViolation,
)
from app.pkg.models.v1.exceptions.user import (
    UserAlreadyExists,
    UserCreateError,
    UserNotFound,
    UserUpdateError,
)

__all__ = ["UserService"]


class UserService:
    """User service class."""

    user_repository: UserRepository
    verify_email: VerifyEmail
    notification_service_client: NotificationServiceClient
    __logger: Logger = get_logger(__name__)

    async def register_user(
        self,
        cmd: models.UserRegisterCommand,
    ) -> models.UserResponse:
        """Registers a new user in the system.

        Args:
            cmd (models.UserRegisterCommand): Command object containing user registration data.

        Returns:
            models.UserResponse: The newly created user details.
        """

        try:
            hashed_password = bcrypt.hash(cmd.user_password)
            user = await self.user_repository.create(
                cmd.migrate(
                    model=models.UserCreateCommand,
                    extra_fields={
                        "hashed_password": hashed_password,
                    },
                ),
            )
            link = await self.verify_email.generate_verification_link(user.user_id)
            await self.notification_service_client.send_email_notification(
                query=models.SendDateNotificationQuery(
                    user_email=user.email,
                    verify_link=link
                ),
            )
            return user
        except UniqueViolation:
            raise UserAlreadyExists
        except DriverError as exc:
            raise UserCreateError from exc

    async def change_password(
        self,
        user: models.User,
        cmd: models.UserChangePasswordCommand,
    ) -> models.UserResponse:
        """Changes the password of the authenticated user.

        Args:
            user (models.User): The currently authenticated user.
            cmd (models.UserChangePasswordCommand): Command object containing old and new passwords.

        Returns:
            models.UserResponse: The updated user with the new password.
        """

        if not check_password(cmd.old_password, user.hashed_password):
            raise InvalidCredentials

        new_hashed_password = bcrypt.hash(cmd.new_password)
        try:
            user = await self.user_repository.update_password(
                cmd=models.UserPasswordUpdateCommand(
                    user_id=user.user_id,
                    hash_password=new_hashed_password,
                ),
            )
            return user
        except EmptyResult:
            raise UserNotFound
        except DriverError as exc:
            raise UserUpdateError from exc

    async def change_data(
        self,
        cmd: models.UserUpdateDataCommand,
    ) -> models.UserResponse:
        """Updates user data with the provided information.

        Args:
            cmd (models.UserUpdateDataCommand): Command containing new user data to update.

        Returns:
            models.UserResponse: The updated user data.
        """
        try:
            return await self.user_repository.update_data(cmd)
        except EmptyResult:
            raise UserNotFound
        except UniqueViolation:
            raise UserAlreadyExists
        except DriverError as exc:
            raise UserUpdateError from exc

    async def verify_user(
        self,
        token: str
    ) -> None:
        """Verifies the user based on the provided verification token.

        Args:
            token (str): Verification token received from the email link.

        Returns:
            None
        """

        try:
            user_id = await self.verify_email.verify_token(token)
            if user_id is None:
                raise UserUpdateError
            await self.user_repository.update_verified(user_id)
        except EmptyResult:
            raise UserNotFound
        except DriverError as exc:
            raise UserUpdateError from exc
