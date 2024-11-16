from django.urls import path, include

from apps.Alerts.views import alert

urlpatterns = [
    path('', include(alert.router.urls), name='AlertManage'),
    path('alert-test/', alert.AlertTestApiView.as_view(), name='alertTest'),
]
