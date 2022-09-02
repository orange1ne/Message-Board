from django.urls import path

from .views import (
    PostList, PostDetail, create_post, PostEdit, PostDelete, subscribe
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/', create_post, name='post_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscribe/', subscribe, name='subscribe'),
]
