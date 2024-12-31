from apps.Task.views import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/V1/logs/<uuid:node_uid>/<uuid:task_uid>/', consumers.LogsConsumer.as_asgi()),
]