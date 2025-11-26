from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # Profile (student or organization)
    path("<str:identifier>/", views.profile_view, name="profile_view"),

    # Follow/unfollow organization
    path("<str:identifier>/follow/", views.follow_organization, name="follow_organization"),

    # Organization tree
    path("organizations/tree/", views.org_tree, name="org_tree"),
]
