from django.urls import path
from . import views
from .views import CommentView, BlogDetailView, MainView


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('home/', views.index, name='home'),
    path('new_post/', views.add, name='new_post'),
    path('<int:id>/detail', BlogDetailView.as_view(), name='post_detail'),
    path('post_edit/<int:pk>/', views.edit, name='post_edit'),
    path('post_delete/<int:pk>/', views.delete, name='post_delete'),
    path('<int:id>/comment/', CommentView.as_view(), name='reviews'),

]