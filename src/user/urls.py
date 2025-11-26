from django.urls import path
from . import views

urlpatterns = [

    # Registration Links
    path("signup/", views.student_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Profile Link
    path("<str:identifier>/", views.profile_view, name="profile_view"),

    # Follow/Unfollow Organization
    path("<str:identifier>/follow/", views.follow_organization, name="follow_organization"),

    # Organization Tree
    path("organizations/tree/", views.org_tree, name="org_tree"),

    # Event CRUD
    path("events/create/", views.create_event, name="create_event"),
    path("<str:username>/event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("<str:username>/event/<int:event_id>/edit/", views.edit_event, name="edit_event"),
    path("<str:username>/event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
]
