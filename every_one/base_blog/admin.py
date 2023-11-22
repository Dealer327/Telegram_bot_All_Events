from django.contrib import admin
from .models import Profile, Event
from .forms import ProfileForm


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ('external_id', 'name', 'time_create', 'time_update', 'choice_month')
    list_display = ('id', 'external_id', 'name', 'time_create', 'time_update', 'choice_month')
    form = ProfileForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_editable = ('name_event', 'info_event', 'publish')
    list_display = ('id', 'name_event', 'info_event', 'user_create', 'start_time', 'create_time', 'publish')
