import requests

from app.sites.base import BaseSite

PRACUJ_PL_API_URL = "https://massachusetts.pracuj.pl/api/offers?jobBoardVersion=2"


class ItPracujPL(BaseSite):
    def run(self) -> None:
        pass

    def retrieve_data(self) -> list[dict] | dict:
        proxy = self.retrieve_random_proxy()
        req = requests.get(PRACUJ_PL_API_URL, proxies=proxy)
        resp = req.json()
        return resp.get("offers", [])

    def check_if_exists_in_db(self, digest_hash: bytes) -> bool:
        query = self._cursor.execute(
            "SELECT hash FROM it_pracuj_pl WHERE hash = %s", (digest_hash,)
        )
        res = query.fetchone()
        return res is not None

    def save_to_db(self, ad_data: dict, digest_hash: bytes) -> None:
        self._cursor.execute(
            "INSERT INTO just_join_it VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                digest_hash,
                ad_data["job_title"],
                ad_data["city"],
                ad_data["exp"],
                ad_data["company"],
                ad_data["skills"],
                ad_data["remote"],
                ad_data["id"],
            ),
        )

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int | list]:
        return {
            "job_title": ad_data["jobTitle"],
            "city": ad_data["location"],
            "id": ad_data["offerId"],
            "job_url": ad_data["offerUrl"],
            "exp": ad_data["employmentLevel"],
            "company": ad_data["employer"],
            "skills": ad_data["technologiesExpected"],
            "remote": ad_data["remoteWork"],
        }
