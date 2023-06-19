import hashlib
import json
import logging
import random
from abc import ABC, abstractmethod

import psycopg
from discord_webhook import DiscordEmbed, DiscordWebhook


class BaseSite(ABC):
    def __init__(
        self,
        filter_data: dict,
        refresh_rate: int,
        proxies_list: list[dict],
        logger: logging.Logger,
        webhook_url: str,
        db_url: str,
    ):
        super().__init__()
        self._filter_data = filter_data
        self._refresh_rate = refresh_rate
        self._proxies_list = proxies_list
        self._logger = logger
        self._webhook_url = webhook_url

        try:
            self._db_conn = psycopg.connect(db_url, autocommit=True)
            self._cursor = self._db_conn.cursor()
        except psycopg.OperationalError as e:
            self._logger.exception(e)
            # TODO: Add better error handling to the db
            exit(1)

    def __del__(self):
        if hasattr(self, "_cursor"):
            self._cursor.close()
        if hasattr(self, "_db_conn"):
            self._db_conn.close()

    @abstractmethod
    def retrieve_data(self) -> list[dict] | dict:
        pass

    @abstractmethod
    def filter(self, data: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def check_if_exists_in_db(self, digest_hash: bytes) -> bool:
        pass

    @abstractmethod
    def save_to_db(self, ad_data: dict, digest_hash: bytes) -> None:
        pass

    @abstractmethod
    def prepare_webhook_data(self, ad_data: dict) -> dict[str, str | int | list]:
        pass

    def send_webhook(self, webhook_data: dict) -> None:
        webhook = DiscordWebhook(
            self._webhook_url, content="New job ad found", rate_limit_retry=True
        )
        embed = DiscordEmbed(
            title=webhook_data["job_title"], url=webhook_data["job_url"]
        )
        embed.add_embed_field(name="Experience", value=webhook_data["exp"])
        embed.add_embed_field(name="Company", value=webhook_data["company"])
        embed.add_embed_field(name="Skills", value=webhook_data["skills"])
        embed.add_embed_field(name="Remote", value=webhook_data["remote"])
        embed.set_timestamp()

        webhook.add_embed(embed)
        webhook.execute()

    def retrieve_random_proxy(self) -> dict[str, str]:
        if self._proxies_list:
            return random.choice(self._proxies_list)
        return {}

    @staticmethod
    def create_hash_from_ad(ad_data: dict) -> bytes:
        dhash = hashlib.md5()
        encoded = json.dumps(ad_data, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.digest()
