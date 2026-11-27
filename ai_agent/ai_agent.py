from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent_page, name='agent_page'),
    path('send/', views.agent_send, name='agent_send'),
]