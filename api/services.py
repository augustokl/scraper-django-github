import requests

from api.models import GitHubUser


def create_github_user(username: str) -> GitHubUser:
    endpoint = f"https://api.github.com/users/{username}"

    r = requests.get(endpoint).json()

    github_user = GitHubUser.objects.create(
        login=r["login"],
        github_id=r["id"],
        name=r["name"],
        blog=r["blog"],
        public_repos=int(r["public_repos"]),
        public_gists=int(r["public_gists"]),
        followers=int(r["followers"]),
        following=int(r["following"]),
        bio=r["bio"],
    )

    return github_user
