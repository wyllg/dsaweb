from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    path("user/", include("user.urls")),

]