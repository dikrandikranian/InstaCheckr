from django.db import models
from django.contrib.auth.models import User

class UserInsights(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    previous_followings = models.JSONField(default=list, blank=True)
    previous_followers = models.JSONField(default=list, blank=True)
    current_followings = models.JSONField(default=list, blank=True)
    current_followers = models.JSONField(default=list, blank=True)
    previous_unfollowers = models.JSONField(default=list, blank=True)
    previous_unfollows = models.JSONField(default=list, blank=True)
    new_unfollowers = models.JSONField(default=list, blank=True)
    new_unfollows = models.JSONField(default=list, blank=True)
    previous_new_followers = models.JSONField(default=list, blank=True)
    previous_new_follows = models.JSONField(default=list, blank=True)
    new_followers = models.JSONField(default=list, blank=True)
    new_follows = models.JSONField(default=list, blank=True)
    non_followers = models.JSONField(default=list, blank=True)
    fans = models.JSONField(default=list, blank=True)
    latest_file_upload = models.DateTimeField(null=True, blank=True)
    previous_file_upload = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Insights for {self.user.username}"
