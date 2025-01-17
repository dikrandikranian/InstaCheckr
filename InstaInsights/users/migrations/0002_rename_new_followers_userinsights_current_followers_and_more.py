# Generated by Django 5.1.4 on 2025-01-01 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinsights',
            old_name='new_followers',
            new_name='current_followers',
        ),
        migrations.RenameField(
            model_name='userinsights',
            old_name='new_followings',
            new_name='current_followings',
        ),
        migrations.RenameField(
            model_name='userinsights',
            old_name='new_unfollowings',
            new_name='new_unfollows',
        ),
        migrations.RenameField(
            model_name='userinsights',
            old_name='old_unfollowings',
            new_name='old_unfollows',
        ),
    ]
