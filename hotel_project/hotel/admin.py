from django.contrib import admin
from .models import Guest, Room, Booking

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'passport_number')
    search_fields = ('first_name', 'last_name', 'passport_number')
    list_filter = ('first_name', 'last_name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'status')
    search_fields = ('room_number', 'room_type')
    list_filter = ('room_type', 'status')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'start_date', 'end_date')
    search_fields = ('guest__first_name', 'guest__last_name', 'room__room_number')
    list_filter = ('start_date', 'end_date')