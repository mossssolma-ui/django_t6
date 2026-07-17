from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import RegisterView, ProfileUserDetailView, ProfileUserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/edit/", ProfileUserUpdateView.as_view(), name="profile_edit"),
    path("profile/user/", ProfileUserDetailView.as_view(), name="profile_user"),
]
