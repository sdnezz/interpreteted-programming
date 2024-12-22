from django.contrib import admin
from .models import Dancer, Group, Schedule

@admin.register(Dancer)
class DancerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'phone_number', 'email', 'unique_id')
    search_fields = ('first_name', 'last_name', 'unique_id')
    list_filter = ('age',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'dance_style', 'status')
    search_fields = ('group_name', 'dance_style')
    list_filter = ('dance_style', 'status')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('dancer', 'group', 'session_date', 'start_time', 'end_time')
    search_fields = ('dancer__first_name', 'dancer__last_name', 'group__group_name')
    list_filter = ('session_date',)
