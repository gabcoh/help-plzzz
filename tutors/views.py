from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
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
