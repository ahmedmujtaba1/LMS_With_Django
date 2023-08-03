from django import forms
from django.forms import TextInput
from diagnostic_centers.models import DiagnosticAdmin, Students, Groups


class AdminLoginForm(forms.ModelForm):
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



class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message here!'}))
