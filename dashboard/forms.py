from django import forms
from django.forms import ModelForm
from .models import Hazard, Person

class HazardForm(ModelForm):
    class Meta:
        model = Hazard
        exclude = ['disaster', 'point', 'weight']

class RescueForm(ModelForm):
    class Meta:
        model = Person
        exclude = ['dob', 'camp', 'point']
