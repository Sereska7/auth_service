"""User repository for PostgresSQL database."""

from abc import ABC
from typing import TypeVar

from app.internal.repository.v1.redis.connection import get_connection


__all__ = ["BaseRedisRepository"]

BaseRepository = TypeVar("BaseRepository", bound="BaseRedisRepository")


class BaseRedisRepository(ABC):
    """Repository for alert manager system."""

    @staticmethod
    async def create(
        redis_key: str,
        redis_value: str,
        expire_time: int | None = None,
    ):
        async with get_connection() as connect:
            await connect.set(redis_key, redis_value)
            if expire_time:
                await connect.expire(redis_key, expire_time)

    @staticmethod
    async def read(
        redis_key: str,
    ):
        async with get_connection() as connect:
            return await connect.get(redis_key)

    @staticmethod
    async def delete(
        redis_key: str,
    ):
        async with get_connection() as connect:
            return await connect.delete(redis_key)
