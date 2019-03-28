from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
                    login_views,
                    register_user,
                    guest_login_views
                )

app_name = "accounts"
urlpatterns = [
    path('login/', login_views,name="login"),
    path('guest-login/', guest_login_views,name="guest-login"),
    path('logout/', LogoutView.as_view(),name="logout"),
    path('register/', register_user,name="register"),
]

