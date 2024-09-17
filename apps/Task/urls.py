from django.urls import path, include

from apps.Task.views import task

urlpatterns = [
    path('', include(task.router.urls), name='TaskManage'),
]
