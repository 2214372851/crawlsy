from apps.Task.views import consumers
from django.urls import path

websocket_urlpatterns = [
    path('logs/<uuid:node_uid>/<uuid:task_uid>/', consumers.LogsConsumer.as_asgi()),
]