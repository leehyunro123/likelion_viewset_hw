from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.
from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer, PostlistSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostlistSerializer
        return PostSerializer
    
    @action(detail=True, methods=['GET'])
    def like(self, request, pk=None):
        like = self.get_object()
        like.likes += 1
        like.save(update_fields=['likes'])
        return Response()
    
    @action(detail=False, methods=['GET'])
    def popular(self, request):
        best_posts = self.get_queryset().order_by('-likes')[:3]
        best_posts_serializer = PostlistSerializer(best_posts, many=True)
        return Response(best_posts_serializer.data)
    
class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post)
        return queryset
    
    #def list(self, request, post_id=None):
    #    post = get_object_or_404(Post, id=post_id)
    #    queryset = self.filter_queryset(self.get_queryset().filter(post=post))
    #    serializer = self.get_serializer(queryset, many=True)
    #    return Response(serializer.data)
    
    #def create(self, request, post_id=None):
    #    post = get_object_or_404(Post, id=post_id)
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save(post=post)
    #    return Response(serializer.data)