""""""

from app.pkg.clients.base_clients import BaseClient
from app.pkg.models import v1 as models

class NotificationServiceClient(BaseClient):
    """Client for interacting with the notification service API."""

    async def send_email_notification(
        self,
        query: models.SendDateNotificationQuery
    ):
        """Sends an email notification request to the notification service.

        Args:
            query (models.SendDateNotificationQuery): Command containing user's email and verification token.
        """

        await self.do_request(
            method="POST",
            path="v1/email/notification/",
            params={
                "user_email": query.user_email,
                "token": query.verify_link,
            },
        )