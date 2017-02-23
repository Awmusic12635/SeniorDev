from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the user index.")


def login(request):
    return render(request, 'login.html', {})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})
