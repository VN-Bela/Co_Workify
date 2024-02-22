from django.urls import path
from .views import (
    Home,
    AboutView,
    ContactView,
    GallaryView,
    PriceView,
    SellerView,
    RetriveWorkspace,
    SpaceImageView,
    DeleteImageview,
    OrganizeView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("gallary/", GallaryView.as_view(), name="gallary"),
    path("price/", PriceView.as_view(), name="price"),
    path("seller/", SellerView.as_view(), name="seller"),
    path("workspace/<int:pk>/", RetriveWorkspace.as_view(), name="RetriveWorkspace"),
    path("spaceimage/<int:pk>/", SpaceImageView.as_view(), name="SpaceImageView"),
    path("deleteImage/<int:pk>/<workspace_id>/", DeleteImageview.as_view(), name="DeleteImageView"),
    path("application", OrganizeView.as_view(), name="application"),

]
