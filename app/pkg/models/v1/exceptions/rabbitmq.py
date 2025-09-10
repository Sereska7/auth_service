"""
Module with RabbitMQ exceptions for the application.
"""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "ErrorPublishToRabbitMQ",
]


class ErrorPublishToRabbitMQ(BaseAPIException):
    message = "Failed to publish message to RabbitMQ."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ErrorRedisRead(BaseAPIException):
    message = "Failed to read entry from Redis."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
