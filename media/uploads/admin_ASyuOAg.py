from django.contrib import admin
from .models import DiagnosticAdmin, Students,Groups, Questionnaire
from django.contrib.auth.models import Group



admin.site.unregister(Group)
admin.site.register(DiagnosticAdmin)
admin.site.register(Students)
admin.site.register(Groups)
admin.site.register(Questionnaire)


