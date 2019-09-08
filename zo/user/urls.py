from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings, name='profile_settings'),
    path('confirm_user_signup/<int:signup_id>', 
         views.confirm_user_signup, name='confirm_user_signup'),
    ]
