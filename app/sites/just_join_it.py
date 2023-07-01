import requests

from ..experience import Experience
from .base import BaseSite, RetrieveException

JUST_JOIN_IT_API_URL = "https://justjoin.it/api/offers"
BASE_JUST_JOIN_IT_URL = "https://justjoin.it/offers/"


class JustJoinIt(BaseSite):
    def retrieve_data(self) -> list[dict]:
        while True:
            try:
                self._logger.info("Retrieving page")

                proxy = self.retrieve_random_proxy()
                req = requests.get(JUST_JOIN_IT_API_URL, proxies=proxy)
                resp = req.json()
                return resp

            except requests.exceptions.RequestException:
                raise RetrieveException

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int | Experience]:
        return {
            "job_title": ad_data["title"],
            "city": ad_data["city"],
            "id": ad_data["id"],
            "job_url": BASE_JUST_JOIN_IT_URL + ad_data["id"],
            "exp": Experience.str_to_enum(ad_data["experience_level"]),
            "company": ad_data["company_name"],
            "skills": "||".join([skill["name"].lower() for skill in ad_data["skills"]]),
            "remote": ad_data["remote"],
        }
