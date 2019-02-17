from django.urls import path

from core.views import (
    home,
    get_shop_info,
    SignUpFormView,
    SignInFormView,
)

app_name = "core"


urlpatterns = [
    path('', home, name="home"),
    path('shop_info', get_shop_info, name="shop_info"),
    path('register/', SignUpFormView.as_view(), name="register"),
    path('login/', SignInFormView.as_view(), name="login"),
]