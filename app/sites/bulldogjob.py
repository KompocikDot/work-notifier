import json

import requests
from bs4 import BeautifulSoup

from app.experience import Experience

from .base import BaseSite, RetrieveException

BULLDOGJOB_BASE_API_URL = (
    "https://bulldogjob.pl/_next/data/{id}/pl/companies/jobs/s/"
    "page,{page}.json?slug=s&slug=page,{page}"
)
BULLDOGJOB_BASE_JOB_URL = "https://bulldogjob.pl/companies/jobs/"


class BulldogJob(BaseSite):
    def retrieve_data(self) -> list[dict]:
        client = requests.Session()
        client.proxies = self.retrieve_random_proxy()

        raw_html = client.get(BULLDOGJOB_BASE_JOB_URL)
        next_build_id = self.parse_nextjs_build_id(raw_html.text)

        ads = []
        page = 1
        params = {"slug": f"page,{page}"}

        while True:
            try:
                self._logger.info(f"Retrieving page {page}")

                url = BULLDOGJOB_BASE_API_URL.format(id=next_build_id, page=page)
                req = client.get(url, params=params)
                res = req.json()

                if jobs := res["pageProps"]["jobs"]:
                    page += 1
                    params["slug"] = f"page,{page}"
                    ads += jobs
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
            "job_title": ad_data["position"],
            "city": ad_data["city"],
            "id": ad_data["id"],
            "job_url": BULLDOGJOB_BASE_JOB_URL + ad_data["id"],
            "exp": Experience.str_to_enum(ad_data["experienceLevel"]),
            "company": ad_data["company"]["name"],
            "skills": "||".join(
                [skill["name"].lower() for skill in ad_data["technologies"]]
            ),
            "remote": ad_data["remote"],
        }

    @staticmethod
    def parse_nextjs_build_id(raw_html: str) -> str:
        scraper = BeautifulSoup(raw_html, "lxml")
        js_build_tag = scraper.find("script", attrs={"id": "__NEXT_DATA__"}).text
        parsed = json.loads(js_build_tag)
        next_build_tag = parsed["buildId"]
        return next_build_tag
