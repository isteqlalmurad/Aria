from django.urls import path
from . import views
from .views import subscribe


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("subscribe/", subscribe, name="subscribe"),
]
