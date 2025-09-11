"""Exceptions for user."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UserNotFound",
    "UserReadError",
    "UserCreateError",
    "UserUpdateError",
    "UserNotVerified",
    "UserAlreadyExists",
    "TokenNotFoundError",
    "VerificationCodeExpiredError",
    "InvalidVerificationPayloadError",
    "InvalidVerificationCodeError",
]


class UserNotFound(BaseAPIException):
    """Exception for a missing user."""

    message = "User not found."
    status_code = status.HTTP_404_NOT_FOUND


class UserReadError(BaseAPIException):
    """Exception for errors when reading by the user."""

    message = "Error deleting user."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserCreateError(BaseAPIException):
    """Exception for errors when reading by the user."""

    message = "Error creating user."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserUpdateError(BaseAPIException):
    """Exception for errors when updating by the user."""

    message = "Error updating user."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserAlreadyExists(BaseAPIException):
    """Exception raised when a user with given unique data already exists."""

    message = "User with this username already exists."
    status_code = status.HTTP_409_CONFLICT


class UserNotVerified(BaseAPIException):
    """Exception for a user whose email is not verified."""

    message = "User email is not verified."
    status_code = status.HTTP_403_FORBIDDEN


class TokenNotFoundError(BaseAPIException):
    """Verifies the email token by checking Redis cache."""

    message = "Token not found."
    status_code = status.HTTP_404_NOT_FOUND


class VerificationCodeExpiredError(BaseAPIException):
    """Exception raised when a verification code is expired or not found in
    Redis."""

    message = "Verification code has expired or is invalid."
    status_code = status.HTTP_404_NOT_FOUND


class InvalidVerificationPayloadError(BaseAPIException):
    """Exception raised when the verification payload in Redis is invalid or
    cannot be decoded."""

    message = "Invalid verification payload."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidVerificationCodeError(BaseAPIException):
    """Exception raised when the provided verification code does not match the
    expected one."""

    message = "Invalid verification code."
    status_code = status.HTTP_400_BAD_REQUEST
