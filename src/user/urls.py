from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('<str:identifier>/', views.profile_view, name='profile'),
]
