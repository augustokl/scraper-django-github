from celery import shared_task

from api.services import create_github_user

from .models import GitHubUser, UserRepository
from .services import GithubConnection


@shared_task(ignore_result=True, acks_late=True)
def get_repository():
    connection = GithubConnection(endpoint="repositories")
    for repository in connection.get_values():
        owner = repository["owner"]
        try:
            github_user = GitHubUser.objects.get(github_id=owner["id"])
        except GitHubUser.DoesNotExist:
            github_user = create_github_user(username=owner["login"])

        UserRepository.objects.update_or_create(
            github_id=repository["id"],
            github_user=github_user,
            defaults={
                "private": repository["private"],
                "description": repository["description"],
                "name": repository["name"],
            },
        )
