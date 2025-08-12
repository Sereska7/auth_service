import secrets

from uuid import UUID

from redis import RedisError

from app.pkg.models.v1.exceptions.user import TokenNotFoundError
from app.pkg.settings import settings
from app.internal.repository.v1 import redis
from app.pkg.models.v1.exceptions.redis import ErrorRedisCreate, ErrorRedisRead


class VerifyEmail:
    """Class responsible for handling email verification."""

    redis_repository: redis.BaseRedisRepository

    async def generate_token(self, user_id: UUID) -> str:
        """Generates a secure email verification token and stores it in Redis with an expiration time.

        Args:
            user_id (UUID): The unique identifier of the user to associate with the token.

        Returns:
            str: A URL-safe token string that can be sent to the user for email verification.
        """

        token = secrets.token_urlsafe(32)
        try:
            await self.redis_repository.create(
                redis_key=f"verify_email:{token}",
                redis_value=str(user_id),
                expire_time=3600
            )
        except RedisError as exc:
            raise ErrorRedisCreate from exc
        return token


    async def generate_verification_link(
        self,
        user_id: UUID,
    ) -> str:
        """Generates an email verification link with a token for the specified user.

        Args:
            user_id (UUID): The user's unique identifier.

        Returns:
            str: A full URL string that the user can use to verify their email.
        """

        token = await self.generate_token(user_id)

        return f"https://{settings.API.HOST}:{settings.API.PORT}/v1/user/verify?token={token}"


    async def verify_token(
        self,
        token: str
    ) -> UUID:
        """Verifies the email token by checking Redis cache.

        Args:
            token (str): The verification token received from the email link.

        Returns:
            UUID: Returns the user ID as UUID if the token is valid.
        """
        try:
            user_id = await self.redis_repository.read(
                redis_key=f"verify_email:{token}",
            )
            if user_id is None:
                raise TokenNotFoundError
            await self.redis_repository.delete(
                redis_key=f"verify_email:{token}"
            )
            user_id = user_id.decode("utf-8")
            return UUID(user_id)
        except RedisError as exc:
            raise ErrorRedisRead from exc
