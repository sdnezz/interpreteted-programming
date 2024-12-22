from django.db import models

class Dancer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    unique_id = models.CharField(max_length=20, unique=True)  # Уникальный ID

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Group(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('inactive', 'Неактивна'),
    ]
    group_name = models.CharField(max_length=100, unique=True)
    dance_style = models.CharField(max_length=50)  # Стиль танца
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Группа {self.group_name} ({self.dance_style})"

class Schedule(models.Model):
    dancer = models.ForeignKey(Dancer, on_delete=models.CASCADE, related_name="schedules")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules")
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.dancer} в {self.group} ({self.session_date})"
