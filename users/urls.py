from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="users-register"),
    path("login/", LoginView.as_view(), name="users-login"),
    path("logout/", LogoutView.as_view(), name="users-logout"),
    path("profile/", ProfileView.as_view(), name="users-profile"),
]
