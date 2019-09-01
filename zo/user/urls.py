from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings, name='profile_settings'),
    ]