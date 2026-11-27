from django.contrib import admin
from .models import AIMessage


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'content', 'created_at')
    list_filter = ('role', 'created_at')


from django.contrib import admin

# Register your models here.
