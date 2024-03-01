from django.urls import path
from .views import loginView, SignUpView,custom_logout,confrim_Registration,BuyerView,AddWorkspaceView,SellerView
# from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("login/", loginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", custom_logout, name="logout"),
    path("sendmail/<int:image_pk>/<str:seller_email>/", confrim_Registration.as_view(), name="sendmail"),
    path("buyer/", BuyerView.as_view(), name="buyer"),
    path("seller/", SellerView.as_view(), name="seller"),
    path("workspace/", AddWorkspaceView.as_view(), name="workspace"),

]
