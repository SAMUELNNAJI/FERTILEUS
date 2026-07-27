from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('new/', views.new_chat, name='new_chat'),
    path('send/', views.send_message, name='send_message'),
    path('history/', views.get_history, name='get_history'),
    path('session/<str:session_id>/', views.load_session, name='load_session'),
]
