from django import forms
from django.forms import ModelForm

from .models import comments


class commentForm(ModelForm):

    class Meta:
        model=comments
        fields ='__all__'