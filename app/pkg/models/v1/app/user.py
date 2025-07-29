"""User models."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import EmailStr
from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class
from app.pkg.models.types import EncryptedSecretBytes

__all__ = [
    "User",
    "ServiceRoleEnum",
    "UserResponse",
    "UserRegisterCommand",
    "UserCreateCommand",
    "UserReadByIDCommand",
    "UserReadByEmailCommand",
    "UserAuthCommand",
    "UserChangePasswordCommand",
    "UserPasswordUpdateCommand"
]


class ServiceRoleEnum(Enum):
    """Enum for service roles."""

    ADMIN = "ADMIN"
    USER = "USER"


class BaseUser(BaseModel):
    """Base model for User."""


class UserFields:
    """User fields."""

    user_id: UUID = Field(
        description="Unique identifier of the user.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    user_email: EmailStr = Field(
        description="Email address of the user.",
        examples=["lolekeektop1@mail.ru", "user@example.com"],
    )
    user_username: EncryptedSecretBytes = Field(
        description="Unique username of the user.",
        examples=["lolekeektop1", "john_doe"],
    )
    user_password: str = Field(
        description="Password of the user.",
        examples=["password"],
    )
    hashed_password: str = Field(
        description="Hashed password of the user.",
        examples=["b'$2b$12$xLgtAEohQUOIw8eaw7iaJOMXRHK/qLSg7i8r6i8hEw6/bmeJuGdpu'"],
    )
    user_is_active: bool = Field(
        description="Indicates whether the user is active.",
        examples=[True, False],
    )
    user_is_verified: bool = Field(
        description="Indicates whether the user's email is verified.",
        examples=[True, False],
    )
    user_service_role: ServiceRoleEnum = Field(
        description="User role name.",
        default=ServiceRoleEnum.USER,
        examples=[ServiceRoleEnum.USER.value, ServiceRoleEnum.ADMIN.value],
    )
    user_create_at: datetime = Field(
        description="Timestamp when the user record was created.",
        examples=["2025-07-21T16:30:00Z"],
    )
    user_update_at: datetime | None = Field(
        description="Timestamp when the user record was last updated.",
        examples=["2025-07-21T16:45:00Z", None],
        default=None,
    )
    old_password: EncryptedSecretBytes = Field(
        description="Old password of the user.",
        examples=["password"],
    )
    new_password: str = Field(
        description="Nwe password of the user.",
        examples=["password"],
    )


OptionalFolderFields = create_optional_fields_class(UserFields)


class User(BaseUser):
    """User model."""

    user_id: UUID = UserFields.user_id
    user_email: EmailStr = UserFields.user_email
    user_username: str = UserFields.user_username
    hashed_password: EncryptedSecretBytes = UserFields.hashed_password
    user_is_active: bool = UserFields.user_is_active
    user_is_verified: bool = UserFields.user_is_verified
    user_service_role: ServiceRoleEnum = UserFields.user_service_role
    user_create_at: datetime = UserFields.user_create_at
    user_update_at: datetime | None = UserFields.user_update_at


class UserResponse(BaseUser):
    """Response model for a user."""

    user_id: UUID = UserFields.user_id
    user_email: EmailStr = UserFields.user_email
    user_username: str = UserFields.user_username
    user_is_active: bool = UserFields.user_is_active
    user_is_verified: bool = UserFields.user_is_verified
    user_service_role: ServiceRoleEnum = UserFields.user_service_role
    user_create_at: datetime = UserFields.user_create_at
    user_update_at: datetime | None = UserFields.user_update_at


# Command.
class UserRegisterCommand(BaseUser):
    """Command model for register new user."""

    user_email: EmailStr = UserFields.user_email
    user_username: str = UserFields.user_username
    user_password: str = UserFields.user_password


class UserCreateCommand(BaseUser):
    """Command model for creating new user."""

    user_email: EmailStr = UserFields.user_email
    user_username: str = UserFields.user_username
    hashed_password: str = UserFields.hashed_password


class UserReadByIDCommand(BaseUser):
    """"""

    user_id: UUID = UserFields.user_id


class UserAuthCommand(BaseUser):
    """"""

    user_email: EmailStr = UserFields.user_email
    user_password: EncryptedSecretBytes = UserFields.user_password


class UserReadByEmailCommand(BaseUser):
    """"""

    user_email: EmailStr = UserFields.user_email


class UserChangePasswordCommand(BaseUser):
    """"""

    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: str = UserFields.new_password


class UserPasswordUpdateCommand(BaseUser):
    """"""

    user_id: UUID = UserFields.user_id
    hash_password: str = UserFields.hashed_password

#Query
