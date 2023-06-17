import binascii
import os

import requests

from .constants import JUST_JOIN_IT_API_URL


class Notifier:
    def __init__(self) -> None:
        pass

    def setup_scraper(self) -> None:
        pass

    def load_proxies(self) -> None:
        pass

    def retrieve_justjoin_data(self) -> dict:
        # Using random hash to bypass cache, it should work,
        # REQUIRES BROADER TESTS
        random_hash = binascii.b2a_hex(os.urandom(5)).decode()
        req = requests.get(JUST_JOIN_IT_API_URL, params={"hash": random_hash})
        resp = req.json()
        return resp

    def filter_advertisements(self) -> dict:
        return {}

    def send_webhook(self) -> None:
        pass
