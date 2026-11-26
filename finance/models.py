from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    TYPE_CHOICES = [('expense', 'Расход'), ('income', 'Доход')]
    name = models.CharField('Название', max_length=100)
    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'categories'

class Operation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата операции', auto_now_add=True)

    class Meta:
        db_table = 'operations'

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    limit_amount = models.DecimalField('Лимит', max_digits=12, decimal_places=2)
    month_year = models.CharField('Месяц и год', max_length=7)

    class Meta:
        db_table = 'budgets'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'password_reset_token'

    def is_valid(self):
        return self.used_at is None and self.expires_at > timezone.now()
# Create your models here.
