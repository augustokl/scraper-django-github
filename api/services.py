import requests

from api.models import GitHubUser


def create_github_user(username: str) -> GitHubUser:
    endpoint = f"https://api.github.com/users/{username}"

    r = requests.get(endpoint).json()

    github_user = GitHubUser.objects.create(
        login=r.get("login"),
        github_id=r["id"],
        name=r.get("name"),
        blog=r.get("blog"),
        public_repos=int(r.get("public_repos")),
        public_gists=int(r.get("public_gists")),
        followers=int(r.get("followers")),
        following=int(r.get("following")),
        bio=r.get("bio"),
    )

    return github_user
