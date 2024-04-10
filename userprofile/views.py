# Create your views here.
# views.py
from django.contrib import admin
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.cache import cache
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from userprofile.models import UserProfile
from .forms import CustomUserCreationForm
from django.contrib import messages


logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Assuming you've removed the handling for additional UserProfile fields here

            # Logging successful registration
            logger.info(f"New user {user.username} has successfully been created.")
            return redirect(
                "login"
            )  # Make sure "login" is a valid named URL in your urls.py
    else:
        form = CustomUserCreationForm()
    return render(request, "userprofile/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Log the count of currently logged-in users

                logger.info(
                    f"User {user.username} logged in successfully. Total online users: {count_online_users()}."
                )
                return render(request, "userprofile/dashboard.html")

            else:
                messages.error(request, "Account is disabled.")
                logger.warning(
                    f"Attempt to login with disabled account: {user.username}"
                )
        else:
            messages.error(request, "Invalid login details.")
            logger.warning(f"Invalid login attempt with username: {username}")
    return render(request, "userprofile/login.html")


def user_logout(request):
    # Logging the logout
    logger.info(f"User {request.user.username} logged out.")

    # clearing the conversation session from vision-bot after user logs_out
    request.session["conversation_history"] = []
    # delete the online status tracker from the chatche key
    # cache.delete(f'online_user_{request.user.pk}')
    logout(request)
    # messages.success(request, 'Logged out successfully.') might use it later for notification
    return redirect("landing")


def count_online_users():
    online_users = 0
    for user in User.objects.all():
        if cache.get(f"online_user_{user.pk}"):
            online_users += 1
    return online_users
