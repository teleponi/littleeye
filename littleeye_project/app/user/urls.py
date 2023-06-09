from django.contrib.auth import views as auth_views
from django.urls import path

from .views import LoginView

app_name = "user"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
]
