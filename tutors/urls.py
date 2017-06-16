from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import Permission
from .views import create_user
# AHHHHHHHHHHHHH

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('help_plz.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/create', create_user, name="create_user"),
]
