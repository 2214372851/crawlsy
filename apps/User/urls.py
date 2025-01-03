from django.urls import path, include

from apps.User.views import user, login, role, permission, menu, operation_log

# 创建操作日志路由
# log_router = DefaultRouter()
# log_router.register(r'operation-logs', operation_log.UserOperationLogViewSet)

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', login.LogoutView.as_view(), name='logout'),
    path('refresh/', login.RefreshTokenView.as_view(), name='refresh'),
    path('profile/', user.UserProfileApiView.as_view(), name='profile'),
    path('feishu/', user.UserFeishuView.as_view(), name='feishu'),
]
urlpatterns += [
    path('', include(user.router.urls), name='UserManage'),
    path('', include(role.router.urls), name='RoleManage'),
    path('', include(permission.router.urls), name='PermissionManage'),
    path('', include(menu.router.urls), name='MenuManage'),
    path('', include(operation_log.router.urls), name='OperationLogManage'),
]
