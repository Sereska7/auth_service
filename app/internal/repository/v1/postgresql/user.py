"""User repository implementation."""

from uuid import UUID

from sqlalchemy import select, update

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models
from app.pkg.models.sqlalchemy_models import User
from app.pkg.models.v1.exceptions.repository import EmptyResult

__all__ = ["UserRepository"]


class UserRepository(Repository):
    """User repository implementation."""

    @collect_response
    async def create(self, cmd: models.UserCreateCommand) -> models.UserResponse:
        """Creates a new user record in the database.

        Args:
            cmd (models.UserCreateCommand): Command object containing user creation data.

        Returns:
            models.UserResponse: The created user details.
        """

        async with get_connection() as session:
            user = User(**cmd.to_dict())
            session.add(user)
            await session.commit()
            await session.refresh(user)

            return models.UserResponse.model_validate(user)

    @collect_response
    async def update_password(
        self,
        cmd: models.UserPasswordUpdateCommand,
    ) -> models.UserResponse:
        """Updates the hashed password of a user.

        Args:
            cmd (models.UserPasswordUpdateCommand): Command object containing user ID and new hashed password.

        Returns:
            models.UserResponse: The updated user details.
        """

        async with get_connection() as session:
            await session.execute(
                update(User)
                .where(User.user_id == cmd.user_id)
                .values(hashed_password=cmd.hash_password),
            )
            await session.commit()
            updated_user = await session.get(User, cmd.user_id)

            return models.UserResponse.model_validate(updated_user)

    @collect_response
    async def get_user_by_id(
        self,
        cmd: models.UserReadByIDCommand,
    ) -> models.UserResponse:
        """Retrieves a user by their unique user ID.

        Args:
            cmd (models.UserReadByIDCommand): Command object containing the user ID.

        Returns:
            models.UserResponse: The user data matching the given ID.
        """

        async with get_connection() as session:
            result = await session.execute(
                select(User).where(User.user_id == cmd.user_id),
            )
            user = result.scalar_one_or_none()

            if user is None:
                raise EmptyResult

            return models.UserResponse.model_validate(user)

    @collect_response
    async def get_full_user_by_id(self, cmd: models.UserReadByIDCommand) -> models.User:
        """Retrieves full user details by user ID.

        Args:
            cmd (models.UserReadByIDCommand): Command object containing the user ID.

        Returns:
            models.User: The full user data corresponding to the given user ID.
        """

        async with get_connection() as session:
            result = await session.execute(
                select(User).where(User.user_id == cmd.user_id),
            )
            user = result.scalar_one_or_none()

            if user is None:
                raise EmptyResult

            return models.User.model_validate(user)

    @collect_response
    async def get_user_by_email(
        self,
        cmd: models.UserReadByEmailCommand,
    ) -> models.User:
        """Retrieves user details by email.

        Args:
            cmd (models.UserReadByEmailCommand): Command object containing the user's email.

        Returns:
            models.User: The user data corresponding to the given email.
        """

        async with get_connection() as session:
            result = await session.execute(
                select(User).where(User.user_email == cmd.user_email),
            )
            user = result.scalar_one_or_none()

            if user is None:
                raise EmptyResult

            return models.User.model_validate(user)

    @collect_response
    async def update_data(
        self,
        cmd: models.UserUpdateDataCommand,
    ) -> models.UserResponse:
        """Updates the user's data in the database.

        Args:
            cmd (models.UserUpdateDataCommand): Command containing the user ID and new data (e.g., new username).

        Returns:
            models.UserResponse: The user object with updated data.
        """
        async with get_connection() as session:
            await session.execute(
                update(User)
                .where(User.user_id == cmd.user_id)
                .values(user_name=cmd.new_user_name),
            )
            await session.commit()
            updated_data = await session.get(User, cmd.user_id)

            return models.UserResponse.model_validate(updated_data)

    @collect_response
    async def update_verified(self, user_id: UUID) -> models.UserResponse:
        """Sets the user's verification status to True in the database.

        Args:
            user_id (UUID): Unique identifier of the user to be marked as verified.

        Returns:
            models.UserResponse: The updated user object with verification status.
        """
        async with get_connection() as session:
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(user_is_verified=True),
            )
            await session.commit()
            updated_data = await session.get(User, user_id)

            return models.UserResponse.model_validate(updated_data)
