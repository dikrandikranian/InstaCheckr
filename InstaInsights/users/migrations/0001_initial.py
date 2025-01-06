# Generated by Django 5.1.4 on 2024-12-29 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInsights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_followings', models.JSONField(blank=True, default=list)),
                ('old_followers', models.JSONField(blank=True, default=list)),
                ('new_followings', models.JSONField(blank=True, default=list)),
                ('new_followers', models.JSONField(blank=True, default=list)),
                ('old_unfollowers', models.JSONField(blank=True, default=list)),
                ('old_unfollowings', models.JSONField(blank=True, default=list)),
                ('new_unfollowers', models.JSONField(blank=True, default=list)),
                ('new_unfollowings', models.JSONField(blank=True, default=list)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
