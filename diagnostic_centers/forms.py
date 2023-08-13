from django import forms
from django.forms import TextInput
from .models import DiagnosticAdmin, Students, Groups
import pandas as pd

class AdminLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DiagnosticAdmin
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control'}),
        }


class StaffLoginForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control'}),
        }


#####################################################################################
from django import forms
from .models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        exclude = ['prediction']
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
        }
    def clean_user(self):
        user = self.cleaned_data['user']
        if Questionnaire.objects.filter(user=user).exists():
            raise forms.ValidationError("Questionnaire already exists for this user.")
        return user


from django import forms
from .models import Groups

class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['name', 'topic', 'student1', 'student2', 'student3', 'supervisor', 'file']



from django import forms
from .models import ProjectUploads

from django import forms
from .models import ProjectUploads

# class ProjectUploadForm(forms.ModelForm):
#     class Meta:
#         model = ProjectUploads
#         fields = ['project_stuff','user', 'title', 'description', 'upload_file', 'remarks']


from django import forms
from .models import ProjectUploads

# class ProjectUploadForm(forms.ModelForm):
#     class Meta:
#         model = ProjectUploads
#         fields = ['user', 'title', 'description', 'upload_file', 'remarks']

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectUploads
        fields = ['user', 'title', 'description', 'upload_file', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make the 'user' field read-only
        self.fields['user'].widget.attrs['readonly'] = 'readonly'
