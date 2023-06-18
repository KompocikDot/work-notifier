import logging
from abc import ABC, abstractmethod
from threading import Thread

from discord_webhook import DiscordEmbed, DiscordWebhook


class BaseSite(ABC, Thread):
    def __init__(
        self,
        filter_data: dict,
        refresh_rate: int,
        logger: logging.Logger,
        webhook_url: str,
    ):
        super().__init__()
        self._filter_data = filter_data
        self._refresh_rate = refresh_rate
        self._logger = logger
        self._webhook_url = webhook_url

    @abstractmethod
    def retrieve_data(self) -> dict:
        pass

    @abstractmethod
    def filter(self, data: dict) -> dict:
        pass

    @abstractmethod
    def check_if_exists_in_db(self, ad_data: dict) -> bool:
        pass

    @abstractmethod
    def save_to_db(self, ad_data: dict) -> None:
        pass

    def send_webhook(self) -> None:
        webhook = DiscordWebhook(
            self._webhook_url, content="New job ad found", rate_limit_retry=True
        )
        embed = DiscordEmbed(title="EXAMPLE JOB", description="Localization: Mars")
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
