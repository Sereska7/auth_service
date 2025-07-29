"""Exceptions for user."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UserNotFound",
    "UserReadError",
    "UserCreateError",
    "UserUpdateError"
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
