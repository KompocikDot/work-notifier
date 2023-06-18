import logging
import os
import random
from threading import Thread

import requests
from dotenv import load_dotenv
from sites.just_join_it import JustJoinIt

LOGGING_FORMAT = "%(asctime)s [%(threadName)s][%(levelname)s] %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler("notifer.log"),
        logging.StreamHandler(),
    ],
)


class Notifier:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.proxies_list: list[dict] = []
        self.filters: dict[str, str | bool | list[str] | None] = {}
        self.webhook_url: str | None = None
        self.refresh_rate: int = 10
        self.client = requests.session()
        self.load_user_variables()
        self.load_proxies()

    def load_user_variables(self) -> None:
        load_dotenv("../envs/.notifier")

        self.filters = {
            "CITY": os.getenv("CITY"),
            "COUNTRY": os.getenv("COUNTRY"),
            "MIN_SALARY": os.getenv("MIN_SALARY"),
            "WORK_TYPE": os.getenv("WORK_TYPE"),
            "KEYWORDS": os.getenv("KEYWORDS", "").split(),
            "REMOTE": bool(os.getenv("REMOTE", False)),
            "EXPERIENCE": os.getenv("EXPERIENCE"),
        }

        self.refresh_rate = int(os.getenv("REFRESH_RATE", 10))
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
                self.logger.warning("No proxies passed")
            else:
                self.logger.info(f"Passed {len(self.proxies_list)} proxies")

    def pick_and_set_proxy(self) -> None:
        picked_proxy: dict[str, str] = random.choice(self.proxies_list)
        self.client.proxies = picked_proxy

    def run_notifier(self) -> None:
        threads = []
        sites_args = [self.filters, self.refresh_rate, self.logger, self.webhook_url]
        sites_objs = [JustJoinIt(*sites_args)]

        for obj in sites_objs:
            t_name = f"{obj.__class__.__name__}-Thread"
            t = Thread(target=obj.run, name=t_name)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
