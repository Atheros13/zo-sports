from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),

    path('settings/', views.settings, name='settings'),
    path('settings_profile/', views.settings_profile, name='settings_profile'),
    path('settings_password/', views.settings_password, name='settings_password'),
    path('settings_email/', views.settings_email, name='settings_email'),

    path('hubs/', views.hubs_main_page, name='user_hubs'),

    path('confirm_user_signup/<int:signup_id>', 
         views.confirm_user_signup, name='confirm_user_signup'),
    ]
