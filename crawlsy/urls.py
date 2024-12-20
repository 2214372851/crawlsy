"""
URL configuration for crawlsy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('doc/schema/', SpectacularAPIView.as_view(), name='schema'),  # schema的配置文件的路由，下面两个ui也是根据这个配置文件来生成的
    path('doc/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger-ui的路由
    path('doc/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc的路由
    path('api/V1/', include('apps.User.urls')),
    path('api/V1/', include('apps.Node.urls')),
    path('api/V1/', include('apps.Task.urls')),
    path('api/V1/', include('apps.Spider.urls')),
    path('api/V1/', include('apps.Ide.urls')),
    path('api/V1/', include('apps.Alerts.urls')),
    path('api/V1/', include('apps.Monitor.urls')),
]
