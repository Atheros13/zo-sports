from django.urls import path
from . import views

urlpatterns = [
    path('<int:hub_id>/', views.hub, name='hub'),
    ]