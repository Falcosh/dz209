
from django.urls import path
from . import views

urlpatterns = [
    # Пустой путь '' будет обрабатывать представление PostListView
    path('', views.PostListView.as_view(), name='post_list'),
]