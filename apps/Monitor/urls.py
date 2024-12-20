from django.urls import path, include

from apps.Monitor.views import monitor

urlpatterns = [
    path('', include(monitor.router.urls), name='Crawlsy'),
]
