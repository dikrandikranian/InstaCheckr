from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os
import re
import zipfile
from django.http import JsonResponse
from bs4 import BeautifulSoup
from users.models import UserInsights
from django.utils.timezone import now
from django.utils.timezone import localtime


def extract_usernames_from_html(file_path):
    """
    Extract Instagram usernames from the provided HTML file.
    """
    usernames = []
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'^https://www.instagram.com/'))
        for link in links:
            username = link.get('href').split('/')[-1]  # Extract username from URL
            if username:
                usernames.append(username)
    return usernames

@login_required
def menus(request):
    try:
        user_insights = UserInsights.objects.get(user=request.user)
        latest_upload_time = localtime(user_insights.latest_file_upload) if user_insights.latest_file_upload else None
        previous_upload_time = localtime(user_insights.previous_file_upload) if user_insights.previous_file_upload else None
        data = {
            "Non Followers": user_insights.non_followers,
            "Fans": user_insights.fans,
            "New Unfollowers": user_insights.new_unfollowers,
            "New Unfollows": user_insights.new_unfollows,
            "New Followers": user_insights.new_followers,
            "New Follows": user_insights.new_follows,
            "Current Followers": user_insights.current_followers,
            "Current Followings": user_insights.current_followings,
            "Previous Unfollowers": user_insights.previous_unfollowers,
            "Previous Unfollows": user_insights.previous_unfollows,
            "Previous New Followers": user_insights.previous_new_followers,
            "Previous New Follows": user_insights.previous_new_follows,
            "Previous Followers": user_insights.previous_followers,
            "Previous Followings": user_insights.previous_followings,
        }
    except UserInsights.DoesNotExist:
        latest_upload_time = None
        previous_upload_time = None
        data = {}

    return render(request, 'menus.html', {
        'data': data,
        'latest_file_upload': latest_upload_time,
        'previous_file_upload': previous_upload_time,
    })

def signout(request):
    logout(request)
    return redirect('home')  # Redirect to home.html in the "users" app

def check_insights(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return JsonResponse({'message': 'No file uploaded.'})

        # Validate the file type
        if not uploaded_file.name.endswith('.zip'):
            return JsonResponse({'message': 'Incorrect file type. Please upload a zip file.'})

        try:
            # Extract the uploaded zip file to a temporary directory
            temp_dir = os.path.join('temp', str(request.user.id))
            os.makedirs(temp_dir, exist_ok=True)
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Check for the "connections" folder
            connections_path = os.path.join(temp_dir, 'connections')
            if not os.path.isdir(connections_path):
                return JsonResponse({'message': 'Incorrect file structure. Please re-fetch data from Instagram and upload again.'})

            # Check for the "followers_and_following" folder inside "connections"
            followers_following_path = os.path.join(connections_path, 'followers_and_following')
            if not os.path.isdir(followers_following_path):
                return JsonResponse({'message': 'Incorrect file structure. Please re-fetch data from Instagram and upload again.'})

            # Look for "following*.html" and "followers*.html"
            following_file = next((f for f in os.listdir(followers_following_path) if f.startswith('following') and f.endswith('.html')), None)
            followers_file = next((f for f in os.listdir(followers_following_path) if f.startswith('followers') and f.endswith('.html')), None)

            if not following_file or not followers_file:
                return JsonResponse({'message': 'Missing required HTML files. Please re-fetch data from Instagram and upload again.'})

            # Extract usernames from "following.html"
            following_file_path = os.path.join(followers_following_path, following_file)
            following_usernames = extract_usernames_from_html(following_file_path)

            # Extract usernames from "followers.html"
            follower_file_path = os.path.join(followers_following_path, followers_file)
            follower_usernames = extract_usernames_from_html(follower_file_path)

            # Update the user's insights
            user_insights = UserInsights.objects.get(user=request.user)

            is_first_upload = user_insights.latest_file_upload is None  # Check if it's the first upload

            user_insights.previous_followings = user_insights.current_followings
            user_insights.previous_followers = user_insights.current_followers
            user_insights.current_followings = following_usernames
            user_insights.current_followers = follower_usernames
            user_insights.previous_unfollowers = user_insights.new_unfollowers
            user_insights.previous_unfollows = user_insights.new_unfollows

            new_unfollowers = [i for i in user_insights.previous_followers if i not in user_insights.current_followers]
            new_unfollows = [i for i in user_insights.previous_followings if i not in user_insights.current_followings]

            user_insights.new_unfollowers = new_unfollowers
            user_insights.new_unfollows = new_unfollows
            user_insights.previous_new_followers = user_insights.new_followers
            user_insights.previous_new_follows = user_insights.new_follows

            if not is_first_upload:

                new_followers = [i for i in user_insights.current_followers if i not in user_insights.previous_followers]
                new_follows = [i for i in user_insights.current_followings if i not in user_insights.previous_followings]

                user_insights.new_followers = new_followers
                user_insights.new_follows = new_follows

            non_followers = [i for i in following_usernames if i not in follower_usernames]
            fans = [i for i in follower_usernames if i not in following_usernames]

            user_insights.non_followers = non_followers
            user_insights.fans = fans

            user_insights.previous_file_upload = user_insights.latest_file_upload  # Shift the latest to previous
            user_insights.latest_file_upload = now()  # Set the current time as latest

            user_insights.save()

            return JsonResponse({'message': f'Success! Instagram account data updated.'})

        except zipfile.BadZipFile:
            return JsonResponse({'message': 'Invalid zip file. Please upload a valid zip file.'})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred. Please try again.'})

    return JsonResponse({'message': 'Invalid request method.'})

def fetch_data(request):
    try:
        user_insights = UserInsights.objects.get(user=request.user)
        data = {
            "Non Followers": user_insights.non_followers,
            "Fans": user_insights.fans,
            "New Unfollowers": user_insights.new_unfollowers,
            "New Unfollows": user_insights.new_unfollows,
            "New Followers": user_insights.new_followers,
            "New Follows": user_insights.new_follows,
            "Current Followers": user_insights.current_followers,
            "Current Followings": user_insights.current_followings,
            "Previous Unfollowers": user_insights.previous_unfollowers,
            "Previous Unfollows": user_insights.previous_unfollows,
            "Previous New Followers": user_insights.previous_new_followers,
            "Previous New Follows": user_insights.previous_new_follows,
            "Previous Followers": user_insights.previous_followers,
            "Previous Followings": user_insights.previous_followings,
        }
    except UserInsights.DoesNotExist:
        data = {}

    return JsonResponse(data)


@login_required
def fetch_upload_times(request):
    try:
        user_insights = UserInsights.objects.get(user=request.user)
        data = {
            "latest_file_upload": localtime(user_insights.latest_file_upload) if user_insights.latest_file_upload else None,
            "previous_file_upload": localtime(user_insights.previous_file_upload) if user_insights.previous_file_upload else None,
        }
    except UserInsights.DoesNotExist:
        data = {
            "latest_file_upload": "Never",
            "previous_file_upload": "Never",
        }
    return JsonResponse(data)