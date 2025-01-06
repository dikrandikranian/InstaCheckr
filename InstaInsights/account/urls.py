from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('menus/', views.menus, name='menus'),
    path('signout/', views.signout, name='signout'),
    path('check-insights/', views.check_insights, name='check_insights'),
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    path('fetch-upload-times/', views.fetch_upload_times, name='fetch_upload_times'),
]