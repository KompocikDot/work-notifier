import requests

from ..experience import Experience
from .base import BaseSite, RetrieveException

NO_FLUFF_JOBS_API_URL = (
    "https://nofluffjobs.com/api/search/"
    "posting?page={page}&salaryCurrency=PLN&salaryPeriod=month&region=pl"
)

NO_FLUFF_JOBS_JOB_URL = "https://nofluffjobs.com/pl/job/"


class NoFluffJobs(BaseSite):
    def retrieve_data(self) -> list[dict]:
        client = requests.Session()
        client.proxies = self.retrieve_random_proxy()

        ads = []
        page = 1
        while True:
            try:
                self._logger.info(f"Retrieving page {page}")

                url = NO_FLUFF_JOBS_API_URL.format(page=page)
                req = client.post(url, json={"rawSearch": ""})
                res = req.json()

                if postings := res["postings"]:
                    ads += postings
                    page += 1
                else:
                    break

            except requests.exceptions.ProxyError:
                self._logger.exception("Proxy error, changing proxy")
                client.proxies = self.retrieve_random_proxy()

            except requests.exceptions.RequestException:
                raise RetrieveException
        return ads

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int | Experience]:
        return {
            "job_title": ad_data["title"],
            "city": ad_data["location"]["places"][0].get("city", ""),
            # TODO: think of it as there are many offers just from one company
            "id": ad_data["id"],
            "job_url": NO_FLUFF_JOBS_JOB_URL + ad_data["url"],
            "exp": Experience.str_to_enum("|".join(ad_data["seniority"])),
            "company": ad_data["name"],
            "skills": ad_data.get("technology", ""),
            "remote": ad_data["fullyRemote"],
        }
