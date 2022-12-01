from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *
from blog.models import Blog


class PostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all().order_by('id')
    serializer_class = BlogSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination


class PostDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogReviewSerializer
    lookup_field = 'id'
