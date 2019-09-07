from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings, name='profile_settings'),
    path('confirm_user_signup/<str:email>/<str:firstname>/<str:surname>/<str:message>', 
         views.confirm_user_signup, name='confirm_user_signup'),
    ]