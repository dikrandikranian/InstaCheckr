from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserInsights

@receiver(post_save, sender=User)
def create_user_insights(sender, instance, created, **kwargs):
    if created:
        UserInsights.objects.create(user=instance)
