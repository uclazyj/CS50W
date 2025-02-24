
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile_page, name="profile_page"),
    path("follow", views.follow_or_unfollow, name="follow_or_unfollow"),
    path("following", views.following, name="following"),
    path("<int:post_id>/edit", views.edit, name="edit"),
    path("<int:post_id>/like", views.like_or_unlike, name="like_or_unlike")
]
