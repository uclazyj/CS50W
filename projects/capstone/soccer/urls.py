from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("team_split", views.team_split, name="team_split"),
    path("player/delete", views.delete_player, name="delete_player"),
    path("player/update", views.update_player, name="update_player"),
    path("players", views.get_players, name="get_players")
]