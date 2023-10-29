from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',

        )
        widgets = {
            'name': forms.TextInput,
            'time_create': forms.DateField,
            'time_update': forms.DateField

        }


