import hashlib
import json
import logging
import random
import time
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

    def run(self) -> None:
        while True:
            jobs_data: list[dict] = self.retrieve_data()
            self._logger.info(f"Found {len(jobs_data)} advertisements")
            if jobs_data:
                if not self._filter_data["SKIP_FILTERS"]:
                    filtered = self.filter(jobs_data)
                    self._logger.info(f"Skipped {len(jobs_data) - len(filtered)} jobs")
                else:
                    filtered = jobs_data
                for ad in filtered:
                    prepared_ad = self.prepare_advert_data(ad)
                    digest = self.create_hash_from_ad(prepared_ad)
                    if not self.check_if_exists_in_db(digest):
                        self.save_to_db(prepared_ad, digest)
                        self.send_webhook(prepared_ad)

            time.sleep(self._refresh_rate)

    @abstractmethod
    def retrieve_data(self) -> list[dict]:
        pass

    @abstractmethod
    def filter(self, data: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int]:
        pass

    def send_webhook(self, webhook_data: dict) -> None:
        webhook = DiscordWebhook(
            self._webhook_url,
            rate_limit_retry=True,
        )
        embed = DiscordEmbed(
            title=webhook_data["job_title"], url=webhook_data["job_url"]
        )
        embed.add_embed_field(name="Experience", value=webhook_data["exp"])
        embed.add_embed_field(name="Company", value=webhook_data["company"])

        skills_arr = webhook_data["skills"].split("||")
        skills = "\n".join([f"- {skill.lower()}" for skill in skills_arr])
        embed.add_embed_field(name="Skills", value=skills)
        embed.add_embed_field(name="Remote", value=webhook_data["remote"])
        embed.add_embed_field(name="City", value=webhook_data["city"])
        embed.set_timestamp()

        webhook.add_embed(embed)
        webhook.execute()

    def retrieve_random_proxy(self) -> dict[str, str]:
        if self._proxies_list:
            return random.choice(self._proxies_list)
        return {}

    def check_if_exists_in_db(self, digest_hash: bytes) -> bool:
        query = self._cursor.execute(
            "SELECT hash FROM workifier_jobs WHERE hash = %s", (digest_hash,)
        )
        res = query.fetchone()
        return res is not None

    def save_to_db(self, ad_data: dict, digest_hash: bytes) -> None:
        print(
            ad_data["skills"],
        )
        self._cursor.execute(
            "INSERT INTO workifier_jobs VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                digest_hash,
                ad_data["job_title"],
                ad_data["city"],
                ad_data["exp"],
                ad_data["company"],
                ad_data["skills"],
                ad_data["remote"],
                ad_data["job_url"],
            ),
        )

    @staticmethod
    def create_hash_from_ad(ad_data: dict) -> bytes:
        dhash = hashlib.md5()
        encoded = json.dumps(ad_data, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.digest()
