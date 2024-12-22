from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('add_dancer/', views.add_dancer, name='add_dancer'),  # Добавить танцора
    path("edit_dancer/<int:dancer_id>/", views.edit_dancer, name="edit_dancer"),  # Редактировать танцора
    path('view_dancers/', views.view_dancers, name='view_dancers'),  # Просмотр танцоров
    path('add_group/', views.add_group, name='add_group'),  # Добавить группу
    path("edit_group/<int:group_id>/", views.edit_group, name="edit_group"),  # Редактировать группу
    path('view_groups/', views.view_groups, name='view_groups'),  # Просмотр групп
    path('add_schedule/', views.add_schedule, name='add_schedule'),  # Добавить расписание
    path('view_schedule/', views.view_schedule, name='view_schedule'),  # Просмотр расписания
    path('tables/', views.show_tables, name='show_tables'),  # Отобразить все таблицы
    path('export/', views.export_to_xml, name='export_to_xml'),  # Экспорт данных
    path('edit_schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('import/', views.import_from_xml, name='import_from_xml'),  # Импорт данных
]
