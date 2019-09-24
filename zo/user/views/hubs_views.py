from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.models import CustomUser, TemporaryPassword
from hub.models import Hub, HubMember

### PROFILE ###

def password_check(user):
    ''' Check if the user has a TemporaryPassword reference, indicating that that
    the user needs to change their password. '''

    if TemporaryPassword.objects.filter(user=user):
        return False
    return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def hubs_main_page(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    h = Hub.objects.filter(members__user=user).filter(members__memberships__is_active)
    if h:
        print(h) 


    return render(
        request,
        'user/hubs.html',
        {
            'title':'Hubs',
            'year':datetime.now().year,
        }
    )