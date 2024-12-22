from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path("edit_guest/<int:guest_id>/",views.edit_guest, name="edit_guest"),
    path('view_guests/', views.view_guests, name='view_guests'),
    path('add_room/', views.add_room, name ='add_room'),
    path("edit_room/<int:room_id>/", views.edit_room, name="edit_room"),
    path('view_rooms/', views.view_rooms, name='view_rooms'),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('tables/', views.show_tables, name ='show_tables'),
    path('export/', views.export_to_xml, name ='export_to_xml'),
    path('import/', views.import_from_xml, name ='import_from_xml'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking')
]