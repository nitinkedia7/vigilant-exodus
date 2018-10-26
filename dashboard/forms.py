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

class PersonForm(ModelForm):
    class Meta:
        model=Person
        exclude = ['emergencyName','emergencyPhone','point']
        widgets = {
            'dob': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY', 'verbose_name': "Date of Birth"}),         
        }

class MissingPersonForm(ModelForm):
    class Meta:
        model=Person
        exclude = ['point','camp','dob']