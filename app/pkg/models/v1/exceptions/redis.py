"""Module with Redis exceptions for the application."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["ErrorRedisCreate", "ErrorRedisRead"]


class ErrorRedisCreate(BaseAPIException):
    message = "Failed to create entry in Redis."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ErrorRedisRead(BaseAPIException):
    message = "Failed to read entry from Redis."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
