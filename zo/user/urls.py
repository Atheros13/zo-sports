from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),

    path('settings/', views.settings, name='settings'),
    path('settings_profile/', views.settings_profile, name='settings_profile'),
    path('settings_password/', views.settings_password, name='settings_password'),
    path('settings_email/', views.settings_email, name='settings_email'),

    path('hubs/', views.hubs_main_page, name='user_hubs'),
    path('contact/', views.contact, name='user_contact'),

    path('confirm_signup/', 
         views.confirm_signup, name='confirm_signup'),
    path('confirm_hub_signup',
         views.confirm_hub_signup, name='confirm_hub_signup'),
    ]
