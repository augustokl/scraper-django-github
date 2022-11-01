import re

import requests
from celery import shared_task

from .models import GitHubUser, UserRepository


@shared_task(ignore_result=True, acks_late=True)
def get_repository():
    endpoint = "https://api.github.com/repositories"
    last_repo = UserRepository.objects.last()

    if last_repo:
        endpoint = f"{endpoint}?since={last_repo.github_id + 1}"

    r = requests.get(endpoint)

    search_pattern = "\<.*?\>"
    re.search(search_pattern, r.headers.get("link"))[0]

    for repository in r.json():
        owner = repository["owner"]
        try:
            github_user = GitHubUser.objects.get(github_id=owner["id"])
        except GitHubUser.DoesNotExist:
            print(owner)

        UserRepository.objects.create(
            github_id=repository["id"],
            private=repository["private"],
            description=repository["description"],
            name=repository["name"],
        )
