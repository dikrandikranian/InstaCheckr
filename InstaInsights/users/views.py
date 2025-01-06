from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import re  # For regex validation
import instaloader


def is_instagram_username_valid(username):
    """
    Check if the given username exists on Instagram using instaloader.
    """
    loader = instaloader.Instaloader()
    try:
        loader.check_profile_id(username)
        return True  # Username exists
    except instaloader.exceptions.ProfileNotExistsException:
        return False  # Username does not exist
    except Exception as e:
        print(f"Error checking Instagram username: {e}")
        return False  # Treat as invalid if an error occurs



def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        #elif not is_instagram_username_valid(username):
        #    messages.error(request, "The username does not exist on Instagram.")
        elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            messages.error(request, "Invalid email address.")
        elif len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[@$!%*?&#]', password):
            messages.error(request, "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            # Create the user
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('signin')  # Redirect to signin page

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the username exists on Instagram
            #if is_instagram_username_valid(username):
                # Log in the user and redirect to menus.html in the "account" app
                # Log in the user and redirect to menus.html in the "account" app
            login(request, user)
            return redirect('account:menus')
            #else:
                # Username no longer exists on Instagram
            #    messages.error(request, "This account can no longer be found on Instagram. Access is denied.")
        else:
            # Display error message
            messages.error(request, "Invalid username or password.")

    return render(request, 'signin.html')
