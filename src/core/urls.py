from django.urls import path

from core.views import home

app_name = "analytics"


urlpatterns = [
    path('', home, name="home"),
]