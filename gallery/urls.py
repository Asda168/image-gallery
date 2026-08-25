from django.urls import path

from . import views

app_name = "gallery"

urlpatterns = [
    path("", views.gallery_home, name="home"),
    path("upload/", views.upload_photo, name="upload"),
    path("photo/<slug:slug>/", views.photo_detail, name="photo_detail"),
    path("photo/<slug:slug>/like/", views.like_photo, name="like_photo"),
]
