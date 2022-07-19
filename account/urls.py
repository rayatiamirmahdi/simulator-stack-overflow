from django.urls import path
from . import views
app_name = "account"
urlpatterns = [
    path("register/", views.RegisterForm.as_view(), name="register_url"),
    path("login/", views.LoginForm.as_view(), name="login_url"),
    path("logout/", views.LogoutUser.as_view(), name="logout_url"),
    path("profile/<int:user_id>", views.ProfileUser.as_view(), name="profile_url"),
    path("follow/<int:user_id>/", views.UserFollowView.as_view(), name="follow_url"),
    path("unfollow/<int:user_id>/", views.UserUnfollowView.as_view(), name="unfollow_url")
]
