from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # <--- Добавили это
    path('agent/', include('agent_app.urls')),  # <--- Замени ai_agent на agent_app
    path('accounts/', include('accounts.urls')), # <--- ЭТА СТРОКА
]
