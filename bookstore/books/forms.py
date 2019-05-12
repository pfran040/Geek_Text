from django import forms
from .models import Comment

class Comment_Form(forms.ModelForm):
    model = Comment
    fields = ['user', 'text-body', 'created']
