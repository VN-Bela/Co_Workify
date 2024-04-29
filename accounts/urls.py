from django.urls import path,include
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
    CustomLoginView,
    SellerProfileView
    
)

# from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("accounts/login/",CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", custom_logout, name="logout"),
    path("",include("django.contrib.auth.urls")),
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
    path("sprofile/", SellerProfileView.as_view(), name="sprofile"),
    
]