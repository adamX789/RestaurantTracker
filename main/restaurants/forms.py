from django import forms
from .models import *

type_list = []
for res in Restaurant.objects.all():
    type_ = res.type
    if type_ not in type_list:
        type_list.append(type_)
choices = [("Všechny", "Všechny")]
for type_ in type_list:
    choices.append((type_, type_))


class MapForm(forms.Form):
    type = forms.ChoiceField(choices=choices,required=True)
