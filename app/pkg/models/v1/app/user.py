"""
User models.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import EmailStr
from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class
from app.pkg.models.types import EncryptedSecretBytes

__all__ = [
    "UserFields",
    "User",
    "ServiceRoleEnum",
    "UserVerifiedEvent",
    "UserResponse",
    "UserRegisterResponse",
    "UserRegisterCommand",
    "UserVerifyCommand",
    "UserCreateCommand",
    "UserReadByIDCommand",
    "UserReadByEmailCommand",
    "UserChangePasswordCommand",
    "UserPasswordUpdateCommand",
    "UserChangeDataCommand",
    "UserUpdateDataCommand",
]


class ServiceRoleEnum(Enum):
    """
    Enum for service roles.
    """

    ADMIN = "ADMIN"
    USER = "USER"


class BaseUser(BaseModel):
    """
    Base model for User.
    """


class UserFields:
    """
    User fields.
    """

    user_id: UUID = Field(
        description="Unique identifier of the user.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    user_email: EmailStr = Field(
        description="Email address of the user.",
        examples=["lolekeektop1@mail.ru", "user@example.com"],
    )
    user_name: str = Field(
        description="Unique user_name of the user.",
        examples=["lolekeektop1", "john_doe"],
    )
    new_user_name: str = Field(
        description="New unique user_name of the user.",
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
        description="New password of the user.",
        examples=["password"],
    )
    event: str = Field(
        default="user.verification.requested",
        description="Type of the event. Always 'user.verification.requested'.",
        examples=["user.verification.requested"],
    )

    event_id: UUID = Field(
        description="Unique identifier of the event (UUID) used for idempotency.",
        examples=["a8d39bb4-0c52-4c56-a21b-34ed4b3f1570"],
    )

    occurred_at: datetime = Field(
        description="Timestamp (UTC) when the event was generated.",
        examples=["2025-09-09T14:10:11.532000+00:00"],
    )

    verification_id: UUID = Field(
        description="UUID of the verification record (key in Redis/DB).",
        examples=["4f7f6f6d-91e7-43aa-bb2f-3dcfb6a2edc4"],
    )
    verification_code: str = Field(
        description="Six-digit verification verification_code (or a magic link).",
        examples=["582341"],
        min_length=6,
        max_length=6,
    )


OptionalFolderFields = create_optional_fields_class(UserFields)


class User(BaseUser):
    """
    User model.
    """

    user_id: UUID = UserFields.user_id
    user_email: EmailStr = UserFields.user_email
    user_name: str = UserFields.user_name
    hashed_password: EncryptedSecretBytes = UserFields.hashed_password
    user_is_active: bool = UserFields.user_is_active
    user_is_verified: bool = UserFields.user_is_verified
    user_service_role: ServiceRoleEnum = UserFields.user_service_role
    user_create_at: datetime = UserFields.user_create_at
    user_update_at: datetime | None = UserFields.user_update_at


class UserVerifiedEvent(BaseUser):
    """ """

    event: str = UserFields.event
    event_id: UUID = UserFields.event_id
    occurred_at: datetime = UserFields.occurred_at
    verification_id: UUID = UserFields.verification_id
    user_id: UUID = UserFields.user_id
    email: EmailStr = UserFields.user_email
    verification_code: str = UserFields.verification_code


class UserResponse(BaseUser):
    """
    Response model for a user.
    """

    user_id: UUID = UserFields.user_id
    user_email: EmailStr = UserFields.user_email
    user_name: str = UserFields.user_name
    user_is_active: bool = UserFields.user_is_active
    user_is_verified: bool = UserFields.user_is_verified
    user_service_role: ServiceRoleEnum = UserFields.user_service_role
    user_create_at: datetime = UserFields.user_create_at
    user_update_at: datetime | None = UserFields.user_update_at


class UserRegisterResponse(BaseUser):
    """
    Register response model for a user.
    """

    user_id: UUID = UserFields.user_id
    user_email: EmailStr = UserFields.user_email
    user_name: str = UserFields.user_name
    user_is_active: bool = UserFields.user_is_active
    user_is_verified: bool = UserFields.user_is_verified
    user_service_role: ServiceRoleEnum = UserFields.user_service_role
    user_create_at: datetime = UserFields.user_create_at
    user_update_at: datetime | None = UserFields.user_update_at
    verification_id: UUID = UserFields.verification_id


# Command.
class UserRegisterCommand(BaseUser):
    """
    Command model for register new user.
    """

    user_email: EmailStr = UserFields.user_email
    user_name: str = UserFields.user_name
    user_password: str = UserFields.user_password


class UserCreateCommand(BaseUser):
    """
    Command model for creating new user.
    """

    user_email: EmailStr = UserFields.user_email
    user_name: str = UserFields.user_name
    hashed_password: str = UserFields.hashed_password


class UserVerifyCommand(BaseUser):
    """
    Command model for verifying email ner user.
    """

    verification_id: UUID = UserFields.verification_id
    code: str = UserFields.verification_code


class UserReadByIDCommand(BaseUser):
    """
    Command model for reading a user by their ID.
    """

    user_id: UUID = UserFields.user_id


class UserReadByEmailCommand(BaseUser):
    """
    Command model for reading a user by their email.
    """

    user_email: EmailStr = UserFields.user_email


class UserChangePasswordCommand(BaseUser):
    """
    Command model for changing the user's password.
    """

    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: str = UserFields.new_password


class UserPasswordUpdateCommand(BaseUser):
    """
    Command model for updating the user's password.
    """

    user_id: UUID = UserFields.user_id
    hash_password: str = UserFields.hashed_password


class UserChangeDataCommand(BaseUser):
    """ """

    new_user_name: str = UserFields.user_name


class UserUpdateDataCommand(BaseUser):
    """
    Command model for updating user data.
    """

    user_id: UUID = UserFields.user_id
    new_user_name: str = UserFields.user_name
