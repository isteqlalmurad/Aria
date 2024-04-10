from django.urls import path
from . import views


urlpatterns = [
    path("read_email/", views.gmail_authenticate, name="read_email"),
    path("oauth2callback/", views.oauth2callback, name="oauth2callback"),
]
