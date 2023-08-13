from django import forms
from .models import Message, Room

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message here!'}))
