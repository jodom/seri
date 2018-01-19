from django import forms

from . import models

class SerieForm(forms.ModelForm):

    class Meta:
        model = models.Serie
        fields = ('title', 'public')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Create a new Serie",
                'id': 'id_title_input'
            }),
        }
