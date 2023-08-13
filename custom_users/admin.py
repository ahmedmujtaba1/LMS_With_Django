from django.contrib import admin
from django.contrib.sites.models import Site

from .models import Profile, Answers, Response

admin.site.register(Profile)
# admin.site.register(Answers)
# admin.site.register(Response)


