import binascii
import os
import time

import requests

from .base import BaseSite

JUST_JOIN_IT_API_URL = "https://justjoin.it/api/offers"


class JustJoinIt(BaseSite):
    def run(self) -> None:
        jobs_data = self.retrieve_data()
        if jobs_data:
            filtered = self.filter(jobs_data)
            if not self.check_if_exists_in_db(filtered):
                self.save_to_db(filtered)

        time.sleep(self._refresh_rate)

    def retrieve_data(self) -> dict:
        # Using random hash to bypass cache, it should work,
        # TODO: Do broader tests
        random_hash = binascii.b2a_hex(os.urandom(5)).decode()
        req = requests.get(JUST_JOIN_IT_API_URL, params={"hash": random_hash})
        resp = req.json()
        return resp

    def filter(self, data: dict) -> dict:
        return {}

    def check_if_exists_in_db(self, ad_data: dict) -> bool:
        return True

    def save_to_db(self, ad_data: dict) -> None:
        pass
