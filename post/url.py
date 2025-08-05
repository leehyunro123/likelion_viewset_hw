from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from post.views import PostViewSet, CommentViewSet, PostCommentViewSet
from rest_framework import routers
from django.urls import path, include

app_name = 'post'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("posts", PostViewSet, basename="posts")

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", PostCommentViewSet, basename="comments") 

post_comment_router = routers.SimpleRouter(trailing_slash=False)
post_comment_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
    path("posts/<int:post_id>/", include(post_comment_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)