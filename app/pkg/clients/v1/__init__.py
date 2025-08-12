"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.clients.v1.notification_service import NotificationServiceClient
from app.pkg.settings import settings

__all__ = [
    "Clients",
]


class Clients(containers.DeclarativeContainer):
    """Declarative container with clients."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    notification_service_client = providers.Factory(
        NotificationServiceClient
    )
    notification_service_client.add_attributes(
        api_url=configuration.CLIENTS.API_URL,
        x_api_token=configuration.CLIENTS.X_API_TOKEN,
    )