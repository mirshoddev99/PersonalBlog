from django.urls import path
from api.views import PostListAPIView, PostDetailAPIView

urlpatterns = [

    path('posts/', PostListAPIView.as_view(), name='posts'),
    path("review/<int:id>/", PostDetailAPIView.as_view(), name="review"),
]
