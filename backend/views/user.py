from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from backend.models import User
import json

def index(request):
    return HttpResponse("Hello, world. You're at the user index.")


def login(request):
    return render(request, 'login.html', {})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})


def get_staff(request):
    print('in get staff')
    staff = User.objects.all().filter(is_staff=1)
    print(staff)
    return HttpResponse(json.dumps({'users': staff}), content_type="application/json")