"""Auth models."""

from pydantic.fields import Field

from app.pkg.models.base import BaseModel


__all__ = [
    "TokenResponse"
]


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


class TokenResponse(BaseAuth):
    """"""

    access_token: str = AuthFields.access_token
    refresh_token: str = AuthFields.refresh_token
    token_type: str = AuthFields.token_type
