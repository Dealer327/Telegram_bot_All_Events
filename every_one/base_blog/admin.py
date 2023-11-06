from django.contrib import admin
from .models import Profile, Event
from .forms import ProfileForm


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'time_create', 'time_update', 'choice_month')
    form = ProfileForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name_event', 'info_event', 'start_time', 'user_create', 'create_time')
