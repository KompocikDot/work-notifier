import requests

from app.sites.base import BaseSite

PRACUJ_PL_API_URL = "https://massachusetts.pracuj.pl/api/offers?jobBoardVersion=2"


class ItPracujPL(BaseSite):
    def retrieve_data(self) -> list[dict]:
        proxy = self.retrieve_random_proxy()
        params = {"pn": 1}
        offers = []

        while True:
            req = requests.get(PRACUJ_PL_API_URL, proxies=proxy, params=params)
            self._logger.info(f"Retrieved page {params['pn']}")

            resp = req.json()
            if pag_offers := resp["offers"]:
                offers += [*pag_offers]
                params["pn"] += 1
            else:
                break
        return offers

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int]:
        return {
            "job_title": ad_data["jobTitle"],
            "city": ad_data["location"],
            "id": ad_data["offerId"],
            "job_url": ad_data["offerUrl"],
            "exp": ad_data["employmentLevel"],
            "company": ad_data["employer"],
            "skills": "||".join(ad_data["technologiesExpected"]),
            "remote": ad_data["remoteWork"],
        }
