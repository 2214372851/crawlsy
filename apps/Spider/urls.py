from django.urls import path, include

from apps.Spider.views import spider

urlpatterns = [
    path('', include(spider.router.urls), name='SpiderManage'),
    path('api/V1/spider-pull/', spider.SpiderPullView.as_view(), name='SpiderPull'),
]
