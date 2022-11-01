from django.db import models


class GitHubUser(models.Model):
    login = models.CharField(max_length=255)
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    blog = models.URLField()
    public_repos = models.IntegerField()
    public_gists = models.IntegerField()
    followers = models.IntegerField()
    following = models.IntegerField()
    bio = models.TextField()


class UserRepository(models.Model):
    name = models.CharField(max_length=255)
    github_user = models.ForeignKey(GitHubUser, on_delete=models.SET_NULL, null=True)
    github_id = models.IntegerField(unique=True)
    private = models.BooleanField()
    description = models.TextField()
