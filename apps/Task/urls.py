from django.urls import path, include

from apps.Task.views import task, scheduler

urlpatterns = [
    path('', include(task.router.urls), name='TaskManage'),
    path('scheduler/', scheduler.SchedulerView.as_view(), name='scheduler'),
    path('scheduler-package/', scheduler.SchedulerPackageView.as_view(), name='schedulerPackage'),
]
