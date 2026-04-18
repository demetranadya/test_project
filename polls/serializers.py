from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from polls.models import Post, Comment, Like
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name = "Post Details",
            summary="Post Details example",
            value={
                "id": 1,
                "title": "Django title",
                "post_text": "Some details about Django",
                "created": "2026-04-18",
                "author": {
                    "id": 1,
                    "first_name": "Надежда",
                    "last_name": "Шаймарданова"
                },
                "comments_count": 3,
                "likes_count": 2

            },
            response_only=True
        ),
        OpenApiExample(
            name = "Post creation",
            summary="Post Create example",
            value={
                "title": "SomeTitle",
                "post_text": "SomeDetails",
                "author": {
                    "id": 1,
                    "first_name": "Надежда",
                    "last_name": "Шаймарданова"
                },
            },
            request_only=True
        ),
    ],
)
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'post_text', 'created',  'author', 'comments_count', 'likes_count']


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'created', 'post', 'user']


class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']