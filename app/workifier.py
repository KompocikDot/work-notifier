import logging
from threading import Thread

from environs import Env
from experience import Experience
from sites.bulldogjob import BulldogJob
from sites.just_join_it import JustJoinIt
from sites.nofluffjobs import NoFluffJobs
from sites.pracuj_pl import ItPracujPL

LOGGING_FORMAT = "%(asctime)s [%(threadName)s][%(levelname)s] %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler("app/notifer.log"),
        logging.StreamHandler(),
    ],
)


class Workifier:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.proxies_list: list[dict] = []
        self.use_proxies: bool = False
        self.filters: dict[str, str | bool | list[str] | None] = {}
        self.webhook_url: str | None = None
        self.refresh_rate: int = 10
        self.db_url: str = ""

        self.load_user_variables()
        self.load_db_envs_and_create_url()

        if self.use_proxies:
            self.load_proxies()

    def load_user_variables(self) -> None:
        env = Env()
        env.read_env("envs/.notifier")

        self.filters = {
            "CITY": env.str("CITY", "").lower(),
            "MIN_SALARY": env.int("MIN_SALARY", 0),
            "WORK_TYPE": env.str("WORK_TYPE", ""),
            "KEYWORDS": [kwd.lower() for kwd in env.list("KEYWORDS", [])],
            "REMOTE": env.bool("REMOTE", False),
            "EXPERIENCE": env.enum(
                "EXPERIENCE", Experience.UNKNOWN, type=Experience, ignore_case=True
            ),
            "SKIP_NO_SALARY": env.bool("SKIP_NO_SALARY", False),
            "SKIP_FILTERS": env.bool("SKIP_FILTERS", False),
        }

        print(self.filters)
        self.use_proxies = env.bool("USE_PROXIES", False)
        self.refresh_rate = env.int("REFRESH_RATE", 10)
        self.webhook_url = env.str("DISCORD_WEBHOOK", "")

    def load_db_envs_and_create_url(self) -> None:
        db_env = Env()
        db_env.read_env("envs/.db")
        postgres_user = db_env.str("POSTGRES_USER", "")
        postgres_pwd = db_env.str("POSTGRES_PASSWORD", "")
        postgres_db = db_env.str("POSTGRES_DB", "")
        self.db_url = (
            f"postgres://{postgres_user}:{postgres_pwd}@localhost:5432/{postgres_db}"
        )

    def load_proxies(self) -> None:
        with open("app/proxies.txt") as f:
            raw_proxies = [line.strip() for line in f.readlines()]
            for raw_proxy in raw_proxies:
                split_count = raw_proxy.count(":")
                if split_count == 4:
                    user, pwd, ip, port = raw_proxy.split(":")
                    proxy = {"http": f"http://{ip}:{port}@{user}:{pwd}"}
                elif split_count == 2:
                    ip, port = raw_proxy.split(":")
                    proxy = {"http": f"http://{ip}:{port}"}
                else:
                    continue

                self.proxies_list.append(proxy)

            if not self.proxies_list:
                self.logger.warning("No proxies passed")
            else:
                self.logger.info(f"Passed {len(self.proxies_list)} proxies")

    def run(self) -> None:
        threads = []
        sites_args = [
            self.filters,
            self.refresh_rate,
            self.proxies_list,
            self.logger,
            self.webhook_url,
            self.db_url,
        ]
        sites_objs = [
            JustJoinIt(*sites_args),
            ItPracujPL(*sites_args),
            BulldogJob(*sites_args),
            NoFluffJobs(*sites_args),
        ]

        for obj in sites_objs:
            t_name = f"{obj.__class__.__name__}-Thread"
            t = Thread(target=obj.run, name=t_name)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
