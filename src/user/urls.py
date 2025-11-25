from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path('organization/<int:org_id>/follow/', views.follow_organization, name='follow_organization'),
    path('organization/<int:org_id>/', views.profile_view, name='organization_profile'),

    path('<str:identifier>/', views.profile_view, name='profile'),

    path("organizations/tree/", views.org_tree, name="org_tree"),
]
