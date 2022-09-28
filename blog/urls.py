from django.urls import path
from . import views
from .views import CommentView


urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.index, name='home'),
    path('new_post/', views.add, name='new_post'),
    path('post/<int:pk>/', views.detail, name='post_detail'),
    path('post_edit/<int:pk>/', views.edit, name='post_edit'),
    path('post_delete/<int:pk>/', views.delete, name='post_delete'),
    path('post_delete/<int:pk>/', views.delete, name='post_delete'),
    path('post/<int:pk>/comment/', CommentView.as_view(), name='add_comment'),

]