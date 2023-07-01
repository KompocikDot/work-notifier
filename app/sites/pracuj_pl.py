import requests

from app.sites.base import BaseSite, RetrieveException

PRACUJ_PL_API_URL = "https://massachusetts.pracuj.pl/api/offers?jobBoardVersion=2"


class ItPracujPL(BaseSite):
    def retrieve_data(self) -> list[dict]:
        client = requests.Session()
        client.proxies = self.retrieve_random_proxy()
        params = {"pn": 1}
        offers = []

        while True:
            try:
                self._logger.info(f"Retrieving page {params['pn']}")

                req = client.get(PRACUJ_PL_API_URL, params=params)
                resp = req.json()

                if pag_offers := resp["offers"]:
                    offers += pag_offers
                    params["pn"] += 1
                else:
                    break

            except requests.exceptions.ProxyError:
                self._logger.exception("Proxy error, changing proxy")
                client.proxies = self.retrieve_random_proxy()

            except requests.exceptions.RequestException:
                raise RetrieveException
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
