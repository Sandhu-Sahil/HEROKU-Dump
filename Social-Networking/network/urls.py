from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('u/<username>', views.profile, name="profile"),
    path('following/', views.following, name="following"),
    path('like/', views.like, name="like"),
    path('follow/', views.follow, name="follow"),
    path('edit_post/', views.edit_post, name="edit"),
    path('addpost/', views.addpost, name="addpost"),
]
