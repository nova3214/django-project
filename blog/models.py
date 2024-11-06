from django.conf import settings
from django.db import models

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Связь с пользователем
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'В ожидании'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')],
        default='pending'
    )