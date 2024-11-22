from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    @property
    def age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"