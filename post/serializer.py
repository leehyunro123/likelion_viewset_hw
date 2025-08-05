from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(use_url=True, required=False)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, instance):
        serialzer = CommentSerializer(instance.comments.all(), many=True)
        return serialzer.data
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image']
        read_only_fields = ['id','created_at', 'updated_at','comments', 'likes']

class PostlistSerializer(serializers.ModelSerializer):
    
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image', 'comments_cnt', 'likes']
        read_only_fields = ['id', 'created_at', 'updated_at', 'comments_cnt', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['id', 'post', 'content', 'like_count', 'created_at', 'updated_at']
        # read_only_fields = ['post']