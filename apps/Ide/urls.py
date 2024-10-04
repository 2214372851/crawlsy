from django.urls import path, include

from apps.Ide.views import ide

urlpatterns = [
    path('ide/', ide.IdeApiView.as_view(), name='IdeManage'),
    path('ide/file/', ide.IdeFileView.as_view(), name='IdeFileManage'),
    path('ide/lazy/', ide.IdeLazyView.as_view(), name='IdeLazyManage'),
]
