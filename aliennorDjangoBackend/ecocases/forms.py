import datetime
from django import forms
from .models import Ecocase
from tinymce.widgets import TinyMCE
from django.contrib.admin import widgets
from django.contrib.auth.models import User


class EcocaseForm(forms.ModelForm):
    title = forms.CharField(max_length=200)

    class Meta:
        model = Ecocase
        fields = ('title',)