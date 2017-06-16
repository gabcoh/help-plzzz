from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import Permission
from .views import create_user, login_view, logout_view
# AHHHHHHHHHHHHH

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('help_plz.urls')),
    url(r'^accounts/login', login_view, name="login"),
    url(r'^accounts/logout', logout_view, name="logout"),
    url(r'^accounts/create', create_user, name="create_user"),
]
