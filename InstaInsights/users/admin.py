from django.contrib import admin
from .models import UserInsights

@admin.register(UserInsights)
class UserInsightsAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user field in the admin list view