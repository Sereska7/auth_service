"""Exceptions for user."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "InvalidCredentials",
    "UserInactive",
    "InvalidTokenPayload",
    "InvalidAuthCredentials",
    "TokenPayloadMissingUserID"
]

class InvalidCredentials(BaseAPIException):
    message = "Invalid email or password."
    status_code = status.HTTP_401_UNAUTHORIZED


class UserInactive(BaseAPIException):
    message = "User is inactive."
    status_code = status.HTTP_403_FORBIDDEN


class InvalidTokenPayload(BaseAPIException):
    message = "Invalid token payload."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidAuthCredentials(BaseAPIException):
    message = "Invalid authentication credentials"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenPayloadMissingUserID(BaseAPIException):
    message = "Token payload missing user_id"
    status_code = status.HTTP_401_UNAUTHORIZED


class IncorrectOldPassword(BaseAPIException):
    message = "Incorrect old password."
    status_code = status.HTTP_400_BAD_REQUEST
