import binascii
import logging
import os
import random

import requests
from constants import JUST_JOIN_IT_API_URL, LOGGING_FORMAT
from discord_webhook import DiscordEmbed, DiscordWebhook

logging.basicConfig(
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler("notifer.log"),
        logging.StreamHandler(),
    ],
)


class Notifier:
    def __init__(self) -> None:
        self.proxies_list: list[dict] = []
        self.filters: dict[str, str | bool | list[str] | None] = {}
        self.webhook_url: str | None = None
        self.client: requests.Session = requests.session()
        self.load_user_variables()
        self.load_proxies()

    def load_user_variables(self) -> None:
        self.filters = {
            "CITY": os.getenv("CITY"),
            "COUNTRY": os.getenv("COUNTRY"),
            "MIN_SALARY": os.getenv("MIN_SALARY"),
            "WORK_TYPE": os.getenv("WORK_TYPE"),
            "KEYWORDS": os.getenv("KEYWORDS", "").split(),
            "REMOTE": bool(os.getenv("REMOTE", False)),
            "EXPERIENCE": os.getenv("EXPERIENCE"),
        }

        self.webhook_url = os.getenv("DISCORD_WEBHOOK")

    def load_proxies(self) -> None:
        with open("proxies.txt") as f:
            raw_proxies = [line.strip() for line in f.readlines()]
            for raw_proxy in raw_proxies:
                user, pwd, ip, port = raw_proxy.split(":")
                if not all([user, pwd, ip, port]):
                    proxy = {"http": f"http://{ip}:{port}"}
                else:
                    proxy = {"http": f"http://{ip}:{port}@{user}:{pwd}"}

                self.proxies_list.append(proxy)

            if not self.proxies_list:
                logging.warning("No proxies passed")
            else:
                logging.info(f"Passed {len(self.proxies_list)} proxies")

    def pick_and_set_proxy(self) -> None:
        picked_proxy: dict[str, str] = random.choice(self.proxies_list)
        self.client.proxies = picked_proxy

    @staticmethod
    def retrieve_justjoin_data() -> dict:
        # Using random hash to bypass cache, it should work,
        # REQUIRES BROADER TESTS
        random_hash = binascii.b2a_hex(os.urandom(5)).decode()
        req = requests.get(JUST_JOIN_IT_API_URL, params={"hash": random_hash})
        resp = req.json()
        return resp

    def filter_advertisements(self) -> dict:
        return {}

    def save_to_db(self, ad_data: dict) -> None:
        pass

    def check_if_present_in_db(self, ad_data: dict) -> None:
        pass

    def send_webhook(self) -> None:
        webhook = DiscordWebhook(
            self.webhook_url, content="New job ad found", rate_limit_retry=True
        )
        embed = DiscordEmbed(title="EXAMPLE JOB", description="Localization: Mars")
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
