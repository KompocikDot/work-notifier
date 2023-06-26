import requests

from .base import BaseSite

NO_FLUFF_JOBS_API_URL = (
    "https://nofluffjobs.com/api/search/"
    "posting?page={page}&salaryCurrency=PLN&salaryPeriod=month&region=pl"
)

NO_FLUFF_JOBS_JOB_URL = "https://nofluffjobs.com/pl/job/"


class NoFluffJobs(BaseSite):
    def retrieve_data(self) -> list[dict]:
        proxy = self.retrieve_random_proxy()
        ads = []
        page = 1
        while True:
            url = NO_FLUFF_JOBS_API_URL.format(page=page)
            self._logger.info(f"Retrieving page {page}")
            req = requests.post(url, json={"rawSearch": ""}, proxies=proxy)
            res = req.json()
            if postings := res["postings"]:
                ads += postings
                page += 1
                break
            else:
                break

        return ads

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int]:
        return {
            "job_title": ad_data["title"],
            "city": ad_data["location"]["places"][0].get("city", ""),
            # TODO: think of it as there are many offers just from one company
            "id": ad_data["id"],
            "job_url": NO_FLUFF_JOBS_JOB_URL + ad_data["url"],
            "exp": "|".join(ad_data["seniority"]),
            "company": ad_data["name"],
            "skills": ad_data.get("technology", ""),
            "remote": ad_data["fullyRemote"],
        }
