from blog.models import Blog, Comment
from rest_framework import serializers
from members.models import CustomUser


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'text']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    subscriber = UserSerializer(read_only=True)

    class Meta:
        depth = 2
        model = Comment
        fields = ('id', 'body', 'subscriber')


class BlogReviewSerializer(serializers.ModelSerializer):
    review = CommentSerializer(read_only=True, many=True, source='comment_set')

    class Meta:
        depth = 3
        model = Blog
        fields = ('id', 'title', 'text', 'review')


