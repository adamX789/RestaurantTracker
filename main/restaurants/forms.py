from django import forms
from .models import *


class MapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Databázový dotaz probíhá až zde, když se formulář vytváří
        type_list = set(Restaurant.objects.values_list('type', flat=True))

        choices = [("Všechny", "Všechny")]
        for type_ in type_list:
            choices.append((type_, type_))

        self.fields['type'] = forms.ChoiceField(choices=choices, required=True)
