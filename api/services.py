import logging
import re
import time
from datetime import datetime
from typing import Generator

import requests
from django.conf import settings

from api.models import GitHubUser

logger = logging.getLogger(__name__)


class GithubConnection:
    base_url = "https://api.github.com"

    def __init__(self, endpoint, many=True) -> None:
        self.token = settings.GITHUB_TOKEN
        self.endpoint_url = f"{self.base_url}/{endpoint}"
        self.many = many

    def _next_page(self, headers):
        search_pattern = "\<(.*?)\>"
        try:
            next = re.search(search_pattern, headers.get("link")).group(1)
        except TypeError:
            return None
        return next

    def _limit_reached(self, headers):
        remaing_limit = int(headers.get("x-ratelimit-remaining"))

        if remaing_limit > 0:
            return False

        release_hour = datetime.fromtimestamp(float(headers.get("x-ratelimit-reset")))
        process_sleep = (release_hour - datetime.now()).total_seconds()

        logger.info(
            "Process will sleep for %d seconds due to the API rate limit", process_sleep
        )
        time.sleep(process_sleep)

    def get_values(self) -> Generator[dict, None, None]:
        endpoint = self.endpoint_url
        while True:
            r = requests.get(endpoint)
            if r.status_code != 200:
                if not self._limit_reached(r.headers):
                    logger.error(r.json())
                    break

            if self.many:
                for item in r.json():
                    print(item)
                    logger.info("Returning item line: %s", item.get("id"))
                    yield item
            else:
                yield r.json()
                break

            next = self._next_page(r.headers)
            if next is None:
                break
            endpoint = next


def create_github_user(username: str) -> GitHubUser:
    connection = GithubConnection(endpoint=f"users/{username}", many=False)
    user_info = next(connection.get_values())

    github_user = GitHubUser.objects.create(
        login=user_info.get("login"),
        github_id=user_info.get("id"),
        name=user_info.get("name"),
        blog=user_info.get("blog"),
        public_repos=int(user_info.get("public_repos", 0)),
        public_gists=int(user_info.get("public_gists", 0)),
        followers=int(user_info.get("followers", 0)),
        following=int(user_info.get("following", 0)),
        bio=user_info.get("bio"),
    )

    return github_user
