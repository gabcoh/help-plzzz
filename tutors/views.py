from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.utils import IntegrityError

# add help_plz:account and create user template


def create_user(request):
    if request.method == "POST":
        if not (all(map(lambda a: a in request.POST, ['password', 'username']))):
            context = {
                'error_message': 'Post error',
            }
            return render(request, 'registration/create_user.html', context)
        new_user = User(
            username=request.POST['username'], password=request.POST['password'])
        try:
            new_user.save()
        except IntegrityError:
            context = {
                'error_message': 'username already taken',
            }
            return render(request, 'registration/create_user.html', context)
        login(request, user=new_user)
        return redirect('help_plz:account')
    else:
        return render(request, 'registration/create_user.html', {})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('help_plz:account')
    if request.method == "POST":
        fields = ["username", "password"]
        if not all(map(lambda field: field in request.POST, fields)):
            context = {
                    'error_message':'You did not provide all required fields',
            }
            return render(request, 'login.html', context)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('help_plz:account')
        else:
            context = {
                    'error_message':'Incorect username or password',
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('help_plz:account')
