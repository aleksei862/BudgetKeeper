from django.db import models
from accounts.models import User


class AIMessage(models.Model):
    ROLE_CHOICES = [('user', 'Пользователь'), ('assistant', 'ИИ-агент')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']


from django.db import models

# Create your models here.
