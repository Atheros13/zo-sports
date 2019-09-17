
from datetime import datetime
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from public import forms, views

urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_sent/', views.password_reset_sent, name='password_reset_sent'),   
    path('password_reset/<str:reset_reference>/', views.password_reset, name='password_reset'),

    path('user/', include('user.urls')),
    path('hub/', include('hub.urls')),

    #path('huttscience/', include('huttscience.urls')),

    path('login/',
         LoginView.as_view
         (
             template_name='public/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('admin/', admin.site.urls),
]
