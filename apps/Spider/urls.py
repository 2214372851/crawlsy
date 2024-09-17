from django.urls import path, include

from apps.Spider.views import spider

urlpatterns = [
    path('', include(spider.router.urls), name='SpiderManage'),
]
