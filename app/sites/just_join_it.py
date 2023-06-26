import requests

from .base import BaseSite

JUST_JOIN_IT_API_URL = "https://justjoin.it/api/offers"
BASE_JUST_JOIN_IT_URL = "https://justjoin.it/offers/"


class JustJoinIt(BaseSite):
    def retrieve_data(self) -> list[dict]:
        proxy = self.retrieve_random_proxy()
        req = requests.get(JUST_JOIN_IT_API_URL, proxies=proxy)
        resp = req.json()
        return resp

    def filter(self, data: list[dict]) -> list[dict]:
        filtered = []
        for row in data:
            # TODO: Dirty trick to not iter n^2 over kwds and user_kwds
            skills_names = "|".join([skill["name"].lower() for skill in row["skills"]])
            user_kwds = self._filter_data["KEYWORDS"]
            if user_kwds:
                kwd_in_skills = any(
                    True for kwd in user_kwds if kwd.lower() in skills_names
                )
                kwd_in_title = any(kwd in row["title"] for kwd in user_kwds)

                if not kwd_in_title and not kwd_in_skills:
                    continue

            if row["remote"] != self._filter_data["REMOTE"]:
                continue
            if not self._filter_data["REMOTE"]:
                if (
                    self._filter_data["CITY"]
                    and row["city"].lower() != self._filter_data["CITY"]
                ):
                    continue
            if self._filter_data["EXPERIENCE"] and (
                self._filter_data["EXPERIENCE"] != row["experience_level"]
            ):
                continue
            # TODO: Add salary filtering later on as it may be really complicated
            filtered.append(row)
        return filtered

    def prepare_advert_data(self, ad_data: dict) -> dict[str, str | int]:
        return {
            "job_title": ad_data["title"],
            "city": ad_data["city"],
            "id": ad_data["id"],
            "job_url": BASE_JUST_JOIN_IT_URL + ad_data["id"],
            "exp": ad_data["experience_level"],
            "company": ad_data["company_name"],
            "skills": "||".join([skill["name"].lower() for skill in ad_data["skills"]]),
            "remote": ad_data["remote"],
        }
