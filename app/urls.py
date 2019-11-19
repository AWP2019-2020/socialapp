from django.urls import path
from app.views import index, PostListView, post_detail

urlpatterns = [
  path('', index, name='post_list'),
  path('', PostListView.as_view(), name='post_list'),
  path('post/<int:pk>', post_detail, name='post_detail'),
]
