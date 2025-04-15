# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from requests import (
    get as http_get,
    post as http_post
)
from logging import getLogger
from os import getenv

class NotificationManager:
    def __init__(self,
                 discord_webhook_url=None):
        self.discord_webhook_url = discord_webhook_url
        self.logger = getLogger("notifications")
        # make sure the webhook url works
        if discord_webhook_url:
            try:
                response = http_get(discord_webhook_url)
                if response.status_code != 200:
                    raise ValueError(
                        f"Discord webhook URL is not valid: {response.status_code}"
                    )
            except Exception as e:
                raise ValueError(f"Discord webhook URL is not valid: {e}") from e
            
            webhook_info = response.json()
            self.logger.info("Discord Webhook URL is valid")
            self.logger.info(f"Webhook Info: name={webhook_info['name']}, id={webhook_info['id']}")
        self.logger.debug("NotificationManager initialized")

    def send_notification(self, message, image_path=None):
        if not self.discord_webhook_url:
            self.logger.warning("No Discord webhook URL provided, notification not sent")
            return

        try:
            if image_path:
                with open(image_path, 'rb') as image_file:
                    files = {'file': (image_path, image_file)}
                    payload = {
                        "content": message
                    }
                    response = http_post(
                        self.discord_webhook_url,
                        data=payload,
                        files=files
                    )
            else:
                response = http_post(
                    self.discord_webhook_url,
                    json={"content": message}
                )

            if response.status_code not in [200, 204]:
                self.logger.error(f"Failed to send notification: {response.status_code}, {response.text}")
                return

        except Exception as e:
            self.logger.error(f"Error whilst sending notification: {e}")
            return

        self.logger.info(f"Notification sent - message: \"{message}\"" + (f", image: \"{image_path}\"" if image_path else ""))

manager = NotificationManager(
    discord_webhook_url=getenv("DISCORD_WEBHOOK_URL")
)

if __name__ == "__main__":
    import logging
    # Test the notification manager
    logging.basicConfig(level=logging.DEBUG)
    manager.send_notification(
        "Test notification",
        image_path="branding/moon.png"
    )
    manager.send_notification(
        "Test notification without image"
    )