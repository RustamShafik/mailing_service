from django.contrib import admin
from .models import Mailing
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Mailing)
