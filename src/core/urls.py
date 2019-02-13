from django.urls import path

from core.views import (
    home,
    SignUpFormView,
    SignInFormView
)

app_name = "core"


urlpatterns = [
    path('', home, name="home"),
    path('register/', SignUpFormView.as_view(), name="register"),
    path('login/', SignInFormView.as_view(), name="login"),
]