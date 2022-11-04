from django.db import models


class GitHubUser(models.Model):
    login = models.CharField(max_length=255)
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True)
    blog = models.URLField(null=True)
    public_repos = models.IntegerField(null=True)
    public_gists = models.IntegerField(null=True)
    followers = models.IntegerField(null=True)
    following = models.IntegerField(null=True)
    bio = models.TextField(null=True)


class UserRepository(models.Model):
    name = models.CharField(max_length=255, null=True)
    github_user = models.ForeignKey(GitHubUser, on_delete=models.SET_NULL, null=True)
    github_id = models.IntegerField(unique=True)
    private = models.BooleanField(null=True)
    description = models.TextField(null=True)
