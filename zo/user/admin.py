from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Gender

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'is_staff']#, 'is_huttscience']
admin.site.register(CustomUser, CustomUserAdmin)

class GenderAdmin(admin.ModelAdmin):
    list_display = ['gender']
admin.site.register(Gender, GenderAdmin)