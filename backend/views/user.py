from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from backend.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the user index.")


def login(request):
    staff = User.objects.all().filter(is_staff=1)
    print(staff)
    return render(request, 'login.html', {'staff':staff})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})
