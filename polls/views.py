from django.shortcuts import render
from django.db.models import Count
# my_app/views.py
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework import status

from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample


def auth(request):
    return render(request, 'oauth.html')


def profile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user_data': serializer.data})

list_view_description = """\
### Get all available posts

Technologies used:
- Django
- DRF
- drf-spectacular

Example API call:

```bash
curl -X GET 'http://127.0.0.1:8000/api/posts/'
```
"""

@extend_schema_view(
    get=extend_schema(
        description=list_view_description,
        responses={
            status.HTTP_200_OK: PostSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="author",
                description="filter by author",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="ordering",
                description="order by a few params",
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        name="Example 1 (created)",
                        description="Order by created date",
                        value="created"
                    ),
                    OpenApiExample(
                        name="Example 2 (likes)",
                        description="Order by count likes",
                        value="likes"
                    ),
                    OpenApiExample(
                        name="Example 3 (comments)",
                        description="Order by count comments",
                        value="comments"
                    ),
                    OpenApiExample(
                        name="Example 4 (title)",
                        description="Order by title",
                        value="title"
                    ),

                ]
            ),

        ]
    ),
)
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.annotate(comments_count=Count('comments'), likes_count=Count('likes'))
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['author', 'created']
    ordering_fields = ['comments_count', 'likes_count']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        # print(self.kwargs)
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post)

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        # print(self.kwargs)
        like_id = self.kwargs['pk']
        return Like.objects.filter(like=like_id)

    def perform_create(self, serializer):
        like_id = self.kwargs['pk']
        post = Post.objects.get(pk=like_id)
        serializer.save(post=post)

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)