"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from polls.views import auth, profile, PostList, PostDetail, CommentList, LikeList
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace="social")),
    path('auth', auth),
    path('accounts/profile/', profile),
    # path('main/', EmptyApiView.as_view(), name='empty-api'),
    # path('', MyView.as_view()),
    path('', PostList.as_view()),
    path("posts/", PostList.as_view()),
    path("posts/<int:pk>/", PostDetail.as_view()),
    path("posts/<int:pk>/comments/", CommentList.as_view()),
    path("posts/<int:pk>/likes/", LikeList.as_view()),

    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs')
]