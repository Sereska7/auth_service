"""Models for User object."""

import json
from datetime import datetime, timezone
from logging import Logger
from uuid import uuid4

from passlib.handlers.bcrypt import bcrypt
from redis import RedisError

from app.internal.pkg.password.password import check_password
from app.internal.pkg.verification.verification import create_verification_code
from app.internal.repository.v1.postgresql.user import UserRepository
from app.internal.repository.v1 import redis, rabbitmq
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.auth import InvalidCredentials
from app.pkg.models.v1.exceptions.redis import ErrorRedisRead
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
    VerificationCodeExpiredError,
    InvalidVerificationPayloadError,
    InvalidVerificationCodeError,
)
from app.pkg.settings import settings

__all__ = ["UserService"]



class UserService:
    """User service class."""

    user_repository: UserRepository
    redis_repository: redis.BaseRedisRepository
    rabbitmq_repository: rabbitmq.RabbitMQRepository
    __logger: Logger = get_logger(__name__)

    async def register_user(
        self,
        cmd: models.UserRegisterCommand,
    ) -> models.UserRegisterResponse:
        """Registers a new user in the system.

        Args:
            cmd (models.UserRegisterCommand): Command object containing user registration data.

        Returns:
            models.UserRegisterResponse: The newly created user details.
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
            verification_code = await create_verification_code()
            verification_id = uuid4()
            redis_key = f"verify:{verification_id}"
            redis_value = json.dumps(
                {
                    "user_id": str(user.user_id),
                    "verification_code": verification_code,
                }
            )
            await self.redis_repository.create(
                redis_key=redis_key,
                redis_value=redis_value,
                expire_time=300
            )
            await self.rabbitmq_repository.create(
                message=models.UserVerifiedEvent(
                    event="user.verification.requested",
                    event_id=uuid4(),
                    occurred_at=datetime.now(timezone.utc),
                    verification_id=verification_id,
                    user_id=user.user_id,
                    email=user.user_email,
                    verification_code=verification_code,
                ),
                routing_key=settings.RABBITMQ.NOTIFICATION_KEY,
            )
            return user.migrate(
                model=models.UserRegisterResponse,
                extra_fields={
                    "verification_id": verification_id
                }
            )
        except UniqueViolation:
            raise UserAlreadyExists
        except DriverError as exc:
            raise UserCreateError from exc


    async def verify_user_email(
        self,
        cmd: models.UserVerifyCommand
    ) -> None:
        """"""

        try:
            data = await self.redis_repository.read(
                redis_key=f"verify:{cmd.verification_id}"
            )
        except RedisError as exc:
            self.__logger.exception("Error reading verification entry from Redis.")
            raise ErrorRedisRead from exc

        if data is None:
            self.__logger.info("Verification code not found or expired.")
            raise VerificationCodeExpiredError

        try:
            code_payload = json.loads(data.decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.__logger.exception("Failed to decode verification payload.")
            raise InvalidVerificationPayloadError from exc

        user_id = code_payload.get("user_id")
        code = code_payload.get("verification_code")

        if code != cmd.code:
            self.__logger.info("Verification code mismatch.")
            raise InvalidVerificationCodeError

        try:
            await self.user_repository.update_verified(user_id)
        except EmptyResult as exc:
            self.__logger.exception("No user found to update verification status.")
            raise UserNotFound from exc
        except DriverError as exc:
            self.__logger.exception("Database error during verification update.")
            raise UserUpdateError from exc

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
