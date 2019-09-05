from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *

# Create your views here.

def hub(request, hub_id):
    assert isinstance(request, HttpRequest)
    
    #h = Hub.objects.get(pk=request.hub_id)

    return render(
        request,
        'hub/hub.html',
        {
            'title':'Hub',
            'message':hub_id,
            'year':datetime.now().year,
        }
    )