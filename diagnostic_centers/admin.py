from django.contrib import admin
from .models import DiagnosticAdmin, Students, Questionnaire
from django.contrib.auth.models import Group

from django.contrib import admin
from django.db import connection

from django.contrib import admin
from diagnostic_centers.models import NewProjectGroup, ProjectUploads
from source.models import Message

admin.site.register(NewProjectGroup)
admin.site.unregister(Group)

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prediction')   

admin.site.register(DiagnosticAdmin)
admin.site.register(Students)
admin.site.register(ProjectUploads)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Message)




