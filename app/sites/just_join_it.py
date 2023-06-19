import time

import requests

from .base import BaseSite

JUST_JOIN_IT_API_URL = "https://justjoin.it/api/offers?limit=1"
BASE_JUST_JOIN_IT_URL = "https://justjoin.it/offers/"


class JustJoinIt(BaseSite):
    def run(self) -> None:
        while True:
            jobs_data: list[dict] = self.retrieve_data()
            self._logger.info(f"Found {len(jobs_data)} advertisements")
            if jobs_data:
                if not self._filter_data["SKIP_FILTERS"]:
                    filtered = self.filter(jobs_data)
                else:
                    filtered = jobs_data
                for ad in filtered:
                    digest = self.create_hash_from_ad(ad)
                    if not self.check_if_exists_in_db(digest):
                        self.save_to_db(ad, digest)
                        webhook_data = self.prepare_webhook_data(ad)
                        self.send_webhook(webhook_data)

            time.sleep(self._refresh_rate)

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
                if row["city"].lower() != self._filter_data["CITY"]:
                    continue
            if self._filter_data["EXPERIENCE"] != row["experience_level"]:
                continue
            # TODO: Add salary filtering later on as it may be really complicated
            filtered.append(row)
        return filtered

    def check_if_exists_in_db(self, digest_hash: bytes) -> bool:
        query = self._cursor.execute(
            "SELECT hash FROM just_join_it WHERE hash = %s", (digest_hash,)
        )
        res = query.fetchone()
        return res is not None

    def save_to_db(self, ad_data: dict, digest_hash: bytes) -> None:
        self._cursor.execute(
            "INSERT INTO just_join_it VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                digest_hash,
                ad_data["title"],
                ad_data["city"],
                ad_data["experience_level"],
                ad_data["company_name"],
                ad_data["published_at"],
                "SKILLS_STR",
                ad_data["remote"],
                ad_data["id"],
            ),
        )

    def prepare_webhook_data(self, ad_data: dict) -> dict[str, str | int | list]:
        return {
            "job_title": ad_data["title"],
            "job_url": BASE_JUST_JOIN_IT_URL + ad_data["id"],
            "exp": ad_data["experience_level"],
            "company": ad_data["company_name"],
            "skills": "[]",
            "remote": ad_data["remote"],
            "published_at": ad_data["published_at"],
        }
