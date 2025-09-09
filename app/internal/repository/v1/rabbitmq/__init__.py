"""RabbitMQ repository container module."""

from dependency_injector import containers, providers
from app.internal.repository.v1.rabbitmq.base_repository import RabbitMQRepository


class Repositories(containers.DeclarativeContainer):
    """RabbitMQ repository container."""

    base_rabbitmq_repository = providers.Factory(RabbitMQRepository)
