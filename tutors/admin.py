from django.contrib import admin
from django.contrib.auth.models import Permission
from help_plz.models import Class

class ClassAdmin(admin.ModelAdmin):
        model= Class 
        filter_horizontal = ('teachers','students','tutors') #If you don't specify this, you will get a multiple select widget.

admin.site.register(Permission)
admin.site.register(Class, ClassAdmin)
