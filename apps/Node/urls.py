from django.urls import path, include

from apps.Node.views import node, search_node

urlpatterns = [
    path('', include(node.router.urls), name='NodeManage'),
    path('node-search/', search_node.SearchNodeView.as_view(), name='nodeSearch'),
]
