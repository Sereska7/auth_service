"""Models for User object."""

from logging import Logger
from passlib.handlers.bcrypt import bcrypt

from app.internal.repository.v1.postgresql.user import UserRepository
from app.internal.pkg.password.password import check_password
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.auth import InvalidCredentials
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult

__all__ = ["UserService"]

from app.pkg.models.v1.exceptions.user import UserCreateError, UserNotFound, UserUpdateError


class UserService:
    """User service class."""

    user_repository: UserRepository
    __logger: Logger = get_logger(__name__)

    async def register_user(
        self,
        cmd: models.UserRegisterCommand,
    ) -> models.UserResponse:
        """
        Registers a new user in the system.

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
                    }
                )
            )
            return user
        except DriverError as exc:
            raise UserCreateError


    async def change_password(
        self,
        user: models.User,
        cmd: models.UserChangePasswordCommand
    ) -> models.UserResponse:
        """
        Changes the password of the authenticated user.

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
                cmd= models.UserPasswordUpdateCommand(
                    user_id=user.user_id,
                    hash_password=new_hashed_password
                )
            )
            return user
        except EmptyResult:
            raise UserNotFound
        except DriverError as exc:
            raise UserUpdateError
