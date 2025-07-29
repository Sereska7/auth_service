"""All jwt repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.pkg.jwt.jwt_handler import JWTHandler


class Repositories(containers.DeclarativeContainer):
    """Container for jwt repositories."""

    jwt_repository = providers.Factory(JWTHandler)