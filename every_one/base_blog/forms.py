from django import forms

from .models import Profile, Event


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


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'external_id',
            'name_event',
            'info_event',
            'start_time',
            'user_create'
        )
        widgets = {
            'name_event': forms.TextInput,
            'info_event': forms.TextInput,
            'start_time': forms.DateTimeField,
            'user_create': forms.TextInput
        }
