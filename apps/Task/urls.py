from django.urls import path, include

from apps.Task.views import task, scheduler, result

urlpatterns = [
    path('', include(task.router.urls), name='TaskManage'),
    path('scheduler/', scheduler.SchedulerView.as_view(), name='scheduler'),
    path('result/', result.TaskResultView.as_view(), name='scheduler'),
    path('scheduler-package/', scheduler.SchedulerPackageView.as_view(), name='schedulerPackage'),
    path('scheduler-extend/', scheduler.SchedulerTaskExtendView.as_view(), name='schedulerExtend'),
]
