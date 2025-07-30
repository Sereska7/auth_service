"""Auth models."""

from pydantic import EmailStr
from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.types import EncryptedSecretBytes
from app.pkg.models.v1.app.user import UserFields

__all__ = ["AuthCommand", "TokenResponse"]


class BaseAuth(BaseModel):
    """Base model for User."""


class AuthFields:
    """User fields."""

    access_token: str = Field(
        description="JWT access token to be used for authenticated requests.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    refresh_token: str = Field(
        description="JWT refresh token to be used for authenticated requests.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        description="Type of the token, usually 'bearer'.",
        examples=["bearer"],
    )


class AuthCommand(BaseAuth):
    """Command model for user authentication (login)."""

    user_email: EmailStr = UserFields.user_email
    user_password: EncryptedSecretBytes = UserFields.user_password


class TokenResponse(BaseAuth):
    """Response model containing access and refresh tokens along with the token
    type."""

    access_token: str = AuthFields.access_token
    refresh_token: str = AuthFields.refresh_token
    token_type: str = AuthFields.token_type
