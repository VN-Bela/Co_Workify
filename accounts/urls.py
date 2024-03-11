from django.urls import path
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from .views import (
    
    SignUpView,
    custom_logout,
    confrim_Registration,
    BuyerView,
    AddWorkspaceView,
    SellerView,
    OrderView,
    PaymentVerificationView,
)

# from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html',authentication_form=LoginForm), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", custom_logout, name="logout"),
    path(
        "sendmail/<int:image_pk>/<str:seller_email>/",
        confrim_Registration.as_view(),
        name="sendmail",
    ),
    path("buyer/", BuyerView.as_view(), name="buyer"),
    path("seller/", SellerView.as_view(), name="seller"),
    path("workspace/", AddWorkspaceView.as_view(), name="workspace"),
    path("order/<int:pk>/", OrderView.as_view(), name="order"),
    path(
        "paymentverification/",
        PaymentVerificationView.as_view(),
        name="paymentverification",
    ),
]
