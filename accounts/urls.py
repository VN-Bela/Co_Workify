from django.urls import path
from .views import loginView, SignUpView,custom_logout
# from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("login/", loginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", custom_logout, name="logout"),
]
